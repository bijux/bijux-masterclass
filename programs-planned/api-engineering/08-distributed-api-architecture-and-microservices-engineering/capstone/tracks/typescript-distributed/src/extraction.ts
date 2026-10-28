import { ValidationError } from "./model.js";

export type ExtractionPhase =
  | "legacy"
  | "shadow"
  | "canary"
  | "cutover"
  | "decommissioned";

export interface Comparison<T> {
  same: boolean;
  legacy: T;
  candidate: T;
}

const ALLOWED: Readonly<Record<ExtractionPhase, ReadonlySet<ExtractionPhase>>> = {
  legacy: new Set(["shadow"]),
  shadow: new Set(["legacy", "canary"]),
  canary: new Set(["shadow", "cutover"]),
  cutover: new Set(["shadow", "canary", "decommissioned"]),
  decommissioned: new Set(),
};

export class StranglerRouter<Arguments extends unknown[], Result> {
  phase: ExtractionPhase = "legacy";
  canaryFraction = 0;
  rollbackAvailable = true;
  readonly comparisons: Comparison<Result>[] = [];

  constructor(
    private readonly legacy: (...args: Arguments) => Result,
    private readonly candidate: (...args: Arguments) => Result,
  ) {}

  transition(phase: ExtractionPhase, canaryFraction = 0): void {
    if (!ALLOWED[this.phase].has(phase)) {
      throw new ValidationError(
        `invalid extraction transition: ${this.phase}->${phase}`,
      );
    }
    if ((phase === "canary" || phase === "cutover") && !this.shadowClean()) {
      throw new ValidationError("promotion requires a clean shadow comparison");
    }
    if (phase === "canary" && !(canaryFraction > 0 && canaryFraction < 1)) {
      throw new ValidationError("invalid canary fraction");
    }
    if (
      (phase === "legacy" || phase === "shadow" || phase === "canary") &&
      (this.phase === "canary" || this.phase === "cutover") &&
      !this.rollbackAvailable
    ) {
      throw new ValidationError("rollback target unavailable");
    }
    if (phase === "cutover" && !this.rollbackAvailable) {
      throw new ValidationError("cutover requires rollback target");
    }
    this.phase = phase;
    this.canaryFraction = canaryFraction;
  }

  call(key: string, ...args: Arguments): Result {
    if (this.phase === "legacy") return this.legacy(...args);
    if (this.phase === "shadow") {
      const oldValue = this.legacy(...args);
      const newValue = this.candidate(...args);
      this.comparisons.push({
        same: JSON.stringify(oldValue) === JSON.stringify(newValue),
        legacy: oldValue,
        candidate: newValue,
      });
      return oldValue;
    }
    if (this.phase === "canary") {
      const bucket = [...new TextEncoder().encode(key)].reduce(
        (total, byte) => total + byte,
        0,
      ) % 10_000;
      return bucket < Math.floor(this.canaryFraction * 10_000)
        ? this.candidate(...args)
        : this.legacy(...args);
    }
    return this.candidate(...args);
  }

  shadowClean(): boolean {
    return this.comparisons.length > 0 &&
      this.comparisons.every((comparison) => comparison.same);
  }
}
