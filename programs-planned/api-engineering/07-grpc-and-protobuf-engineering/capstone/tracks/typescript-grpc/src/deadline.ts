export interface Clock { nowSeconds(): number; }

export class Deadline {
  public constructor(
    private readonly expiresAt: number,
    private readonly clock: Clock,
  ) {}

  public static after(seconds: number, clock: Clock): Deadline {
    if (seconds <= 0) throw new Error("deadline must be positive");
    return new Deadline(clock.nowSeconds() + seconds, clock);
  }

  public remaining(): number {
    return Math.max(0, this.expiresAt - this.clock.nowSeconds());
  }

  public childTimeout(reserve = 0, cap?: number): number {
    const value = Math.max(0, this.remaining() - reserve);
    return cap === undefined ? value : Math.min(value, cap);
  }
}

export interface RetryPolicy {
  readonly maxAttempts: number;
  readonly initialBackoff: number;
  readonly multiplier: number;
  readonly maxBackoff: number;
  readonly retryableStatuses: ReadonlySet<string>;
}

export function retryDelay(
  policy: RetryPolicy,
  retryIndex: number,
  jitter: number,
): number {
  const raw = Math.min(
    policy.maxBackoff,
    policy.initialBackoff * policy.multiplier ** retryIndex,
  );
  return raw * Math.max(0, Math.min(1, jitter));
}

export function retryAllowed(input: {
  policy: RetryPolicy;
  method: string;
  status: string;
  attempt: number;
  idempotent: boolean;
  remaining: number;
  nextDelay: number;
}): boolean {
  return input.attempt < input.policy.maxAttempts
    && input.policy.retryableStatuses.has(input.status)
    && (input.method.startsWith("Get") || input.idempotent)
    && input.nextDelay < input.remaining;
}
