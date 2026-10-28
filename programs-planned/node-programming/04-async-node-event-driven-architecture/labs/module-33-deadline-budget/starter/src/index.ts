export class Budget {
  constructor(
    readonly deadline: number,
    private readonly now: () => number,
  ) {}

  remaining(): number {
    return Math.max(0, this.deadline - this.now());
  }

  child(maximumMilliseconds: number): Budget {
    return new Budget(
      Math.min(this.deadline, this.now() + maximumMilliseconds),
      this.now,
    );
  }
}
