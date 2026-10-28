export class BulkheadFull extends Error {}

export class Bulkhead {
  private inUseValue = 0;
  public constructor(public readonly limit: number) {
    if (!Number.isSafeInteger(limit) || limit < 1) throw new Error("bulkhead limit must be positive");
  }
  public get inUse(): number { return this.inUseValue; }
  public acquire(): () => void {
    if (this.inUseValue >= this.limit) throw new BulkheadFull("dependency concurrency limit reached");
    this.inUseValue += 1;
    let released = false;
    return () => {
      if (!released) {
        released = true;
        this.inUseValue -= 1;
        if (this.inUseValue < 0) throw new Error("bulkhead permit underflow");
      }
    };
  }
}
