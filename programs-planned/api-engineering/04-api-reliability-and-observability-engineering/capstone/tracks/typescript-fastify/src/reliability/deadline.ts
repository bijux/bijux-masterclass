import type { Clock } from "./clock.js";

export class DeadlineExceeded extends Error {}

export class Deadline {
  public constructor(public readonly expiresAtMs: number) {
    if (!Number.isSafeInteger(expiresAtMs)) throw new Error("deadline must be a safe integer");
  }
  public static after(clock: Clock, timeoutMs: number): Deadline {
    if (!Number.isSafeInteger(timeoutMs) || timeoutMs <= 0) throw new Error("timeout must be positive");
    return new Deadline(clock.nowMs() + timeoutMs);
  }
  public remainingMs(clock: Clock): number { return Math.max(0, this.expiresAtMs - clock.nowMs()); }
  public requireRemaining(clock: Clock, minimumMs = 1): number {
    const remaining = this.remainingMs(clock);
    if (remaining < minimumMs) throw new DeadlineExceeded("operation deadline exhausted");
    return remaining;
  }
  public child(clock: Clock, maximumMs: number): Deadline {
    if (maximumMs <= 0) throw new Error("child maximum must be positive");
    return new Deadline(Math.min(this.expiresAtMs, clock.nowMs() + maximumMs));
  }
}
