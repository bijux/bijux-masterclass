import type { Clock } from "./clock.js";

export type CircuitState = "closed" | "open" | "half-open";
export class CircuitOpen extends Error {}

export class CircuitBreaker {
  public state: CircuitState = "closed";
  public consecutiveFailures = 0;
  public openedAtMs: number | undefined;
  public halfOpenInFlight = 0;

  public constructor(
    public readonly failureThreshold: number,
    public readonly openDurationMs: number,
    public readonly halfOpenMaxCalls = 1,
  ) {
    if (!Number.isSafeInteger(failureThreshold) || failureThreshold < 1) {
      throw new Error("failureThreshold must be positive");
    }
    if (!Number.isSafeInteger(openDurationMs) || openDurationMs < 1) {
      throw new Error("openDurationMs must be positive");
    }
    if (!Number.isSafeInteger(halfOpenMaxCalls) || halfOpenMaxCalls < 1) {
      throw new Error("halfOpenMaxCalls must be positive");
    }
  }

  public allow(clock: Clock): void {
    if (this.state === "open") {
      if (this.openedAtMs === undefined) throw new Error("open circuit lacks timestamp");
      if (clock.nowMs() - this.openedAtMs < this.openDurationMs) {
        throw new CircuitOpen("dependency circuit is open");
      }
      this.state = "half-open";
      this.halfOpenInFlight = 0;
    }
    if (this.state === "half-open") {
      if (this.halfOpenInFlight >= this.halfOpenMaxCalls) {
        throw new CircuitOpen("half-open probe already in flight");
      }
      this.halfOpenInFlight += 1;
    }
  }

  public success(): void {
    this.state = "closed";
    this.consecutiveFailures = 0;
    this.openedAtMs = undefined;
    this.halfOpenInFlight = 0;
  }

  public failure(clock: Clock): void {
    if (this.state === "half-open") {
      this.open(clock);
      return;
    }
    this.consecutiveFailures += 1;
    if (this.consecutiveFailures >= this.failureThreshold) this.open(clock);
  }

  public abandonProbe(clock: Clock): void {
    if (this.state === "half-open" && this.halfOpenInFlight > 0) this.open(clock);
  }

  private open(clock: Clock): void {
    this.state = "open";
    this.openedAtMs = clock.nowMs();
    this.halfOpenInFlight = 0;
  }
}
