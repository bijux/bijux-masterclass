function lengthPrefix(value: string): string {
  return `${value.length}:${value}`;
}

export interface CacheKeyInput {
  tenantId: string;
  policyPartition: string;
  resourceType: string;
  resourceId: string;
  version: string;
  representation: string;
}

export interface AuthorizedCacheKey extends CacheKeyInput {
  canonical: string;
}

export function createAuthorizedCacheKey(input: CacheKeyInput): AuthorizedCacheKey {
  const values = [
    input.tenantId,
    input.policyPartition,
    input.resourceType,
    input.resourceId,
    input.version,
    input.representation,
  ];
  if (values.some((value) => value.length === 0)) {
    throw new Error("cache key fields must be non-empty");
  }
  return { ...input, canonical: values.map(lengthPrefix).join("|") };
}

interface CacheEntry<T> {
  value: T;
  expiresAtNs: bigint;
  sizeBytes: bigint;
  classification: "positive" | "negative";
}

export interface CacheLookup<T> {
  state: "hit" | "miss" | "stale";
  value?: T;
}

export class BoundedTTLCache<T> {
  private readonly entries = new Map<string, CacheEntry<T>>();
  private bytes = 0n;
  private hits = 0;
  private misses = 0;
  private stale = 0;
  private evictions = 0;

  constructor(
    readonly maxEntries: number,
    readonly maxBytes: bigint,
  ) {
    if (!Number.isSafeInteger(maxEntries) || maxEntries <= 0 || maxBytes <= 0n) {
      throw new Error("cache bounds must be positive");
    }
  }

  get(key: AuthorizedCacheKey, nowNs: bigint): CacheLookup<T> {
    const entry = this.entries.get(key.canonical);
    if (entry === undefined) {
      this.misses += 1;
      return { state: "miss" };
    }
    if (nowNs >= entry.expiresAtNs) {
      this.entries.delete(key.canonical);
      this.bytes -= entry.sizeBytes;
      this.stale += 1;
      return { state: "stale" };
    }
    this.entries.delete(key.canonical);
    this.entries.set(key.canonical, entry);
    this.hits += 1;
    return { state: "hit", value: entry.value };
  }

  put(
    key: AuthorizedCacheKey,
    value: T,
    input: {
      nowNs: bigint;
      ttlNs: bigint;
      sizeBytes: bigint;
      classification?: "positive" | "negative";
    },
  ): void {
    if (input.ttlNs <= 0n || input.sizeBytes < 0n) throw new Error("invalid entry");
    const existing = this.entries.get(key.canonical);
    if (existing !== undefined) {
      this.entries.delete(key.canonical);
      this.bytes -= existing.sizeBytes;
    }
    if (input.sizeBytes > this.maxBytes) return;
    const entry: CacheEntry<T> = {
      value,
      expiresAtNs: input.nowNs + input.ttlNs,
      sizeBytes: input.sizeBytes,
      classification: input.classification ?? "positive",
    };
    this.entries.set(key.canonical, entry);
    this.bytes += entry.sizeBytes;
    while (this.entries.size > this.maxEntries || this.bytes > this.maxBytes) {
      const oldest = this.entries.keys().next().value as string | undefined;
      if (oldest === undefined) break;
      const removed = this.entries.get(oldest);
      this.entries.delete(oldest);
      if (removed !== undefined) this.bytes -= removed.sizeBytes;
      this.evictions += 1;
    }
  }

  snapshot(): Record<string, string | number> {
    return {
      entries: this.entries.size,
      estimatedBytes: this.bytes.toString(),
      hits: this.hits,
      misses: this.misses,
      stale: this.stale,
      evictions: this.evictions,
    };
  }

  clear(): void {
    this.entries.clear();
    this.bytes = 0n;
  }
}
