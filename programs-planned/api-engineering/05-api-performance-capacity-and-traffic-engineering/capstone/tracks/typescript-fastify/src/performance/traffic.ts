export interface BucketState {
  tokens: bigint;
  lastNs: bigint;
  remainder: bigint;
}

export interface TokenDecision {
  allowed: boolean;
  remaining: bigint;
  retryAfterNs?: bigint;
  reason: string;
}

export class TokenBucket {
  static readonly NS = 1_000_000_000n;
  private tokens: bigint;
  private lastNs: bigint;
  private remainder = 0n;

  constructor(
    readonly capacity: bigint,
    readonly refillPerSecond: bigint,
    initialTokens = capacity,
    initialNs = 0n,
  ) {
    if (capacity <= 0n || refillPerSecond <= 0n) {
      throw new Error("bucket capacity and refill must be positive");
    }
    if (initialTokens < 0n || initialTokens > capacity || initialNs < 0n) {
      throw new Error("invalid initial bucket state");
    }
    this.tokens = initialTokens;
    this.lastNs = initialNs;
  }

  get state(): BucketState {
    return { tokens: this.tokens, lastNs: this.lastNs, remainder: this.remainder };
  }

  restore(state: BucketState): void {
    if (
      state.tokens < 0n ||
      state.tokens > this.capacity ||
      state.lastNs < 0n ||
      state.remainder < 0n ||
      state.remainder >= TokenBucket.NS
    ) {
      throw new Error("invalid restored state");
    }
    this.tokens = state.tokens;
    this.lastNs = state.lastNs;
    this.remainder = state.remainder;
  }

  private refill(nowNs: bigint): void {
    if (nowNs < this.lastNs) throw new Error("monotonic time moved backward");
    const elapsed = nowNs - this.lastNs;
    const numerator = elapsed * this.refillPerSecond + this.remainder;
    const added = numerator / TokenBucket.NS;
    const nextRemainder = numerator % TokenBucket.NS;
    this.tokens = this.tokens + added < this.capacity ? this.tokens + added : this.capacity;
    this.lastNs = nowNs;
    this.remainder = this.tokens === this.capacity ? 0n : nextRemainder;
  }

  consume(nowNs: bigint, cost: bigint): TokenDecision {
    if (cost <= 0n) throw new Error("cost must be positive");
    this.refill(nowNs);
    if (cost <= this.tokens) {
      this.tokens -= cost;
      return { allowed: true, remaining: this.tokens, reason: "allowed" };
    }
    const missing = cost - this.tokens;
    const numerator = missing * TokenBucket.NS - this.remainder;
    const retry =
      numerator <= 0n
        ? 0n
        : (numerator + this.refillPerSecond - 1n) / this.refillPerSecond;
    return {
      allowed: false,
      remaining: this.tokens,
      retryAfterNs: retry,
      reason: "token-budget",
    };
  }
}

export function reserveAtomically(
  requests: readonly { bucket: TokenBucket; cost: bigint }[],
  nowNs: bigint,
): { allowed: boolean; reason: string; retryAfterNs?: bigint } {
  const states = requests.map(({ bucket }) => bucket.state);
  for (let index = 0; index < requests.length; index += 1) {
    const item = requests[index];
    if (item === undefined) throw new Error("internal reservation error");
    const decision = item.bucket.consume(nowNs, item.cost);
    if (!decision.allowed) {
      requests.forEach(({ bucket }, restoreIndex) => {
        const state = states[restoreIndex];
        if (state === undefined) throw new Error("internal rollback error");
        bucket.restore(state);
      });
      return {
        allowed: false,
        reason: `budget-${index}`,
        ...(decision.retryAfterNs === undefined
          ? {}
          : { retryAfterNs: decision.retryAfterNs }),
      };
    }
  }
  return { allowed: true, reason: "allowed" };
}

export class LimiterRegistry {
  private readonly entries = new Map<string, { bucket: TokenBucket; lastUsed: bigint }>();

  constructor(
    readonly maxKeys: number,
    readonly idleTtlNs: bigint,
    readonly capacity: bigint,
    readonly refillPerSecond: bigint,
  ) {
    if (maxKeys <= 0 || idleTtlNs <= 0n) throw new Error("invalid registry bounds");
  }

  bucket(key: string, nowNs: bigint): TokenBucket {
    for (const [existingKey, entry] of [...this.entries.entries()].sort()) {
      if (nowNs - entry.lastUsed >= this.idleTtlNs) this.entries.delete(existingKey);
    }
    const existing = this.entries.get(key);
    if (existing !== undefined) {
      existing.lastUsed = nowNs;
      return existing.bucket;
    }
    if (this.entries.size >= this.maxKeys) throw new Error("limiter-key-capacity");
    const bucket = new TokenBucket(this.capacity, this.refillPerSecond, this.capacity, nowNs);
    this.entries.set(key, { bucket, lastUsed: nowNs });
    return bucket;
  }

  get size(): number {
    return this.entries.size;
  }
}
