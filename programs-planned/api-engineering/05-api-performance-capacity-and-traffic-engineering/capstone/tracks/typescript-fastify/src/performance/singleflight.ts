export class SingleFlightRejected extends Error {}

export class SingleFlight<T> {
  private readonly tasks = new Map<string, Promise<T>>();
  private readonly waiters = new Map<string, number>();

  constructor(
    readonly maxConcurrentFills: number,
    readonly maxWaitersPerKey: number,
  ) {
    if (maxConcurrentFills <= 0 || maxWaitersPerKey <= 0) {
      throw new Error("single-flight bounds must be positive");
    }
  }

  async do(
    key: string,
    factory: () => Promise<T>,
    timeoutMs?: number,
  ): Promise<T> {
    if (!key) throw new Error("single-flight key is required");
    let task = this.tasks.get(key);
    if (task === undefined) {
      if (this.tasks.size >= this.maxConcurrentFills) {
        throw new SingleFlightRejected("fill-capacity");
      }
      task = factory().finally(() => {
        if (this.tasks.get(key) === task) this.tasks.delete(key);
      });
      this.tasks.set(key, task);
    }
    const currentWaiters = this.waiters.get(key) ?? 0;
    if (currentWaiters >= this.maxWaitersPerKey) {
      throw new SingleFlightRejected("waiter-capacity");
    }
    this.waiters.set(key, currentWaiters + 1);
    try {
      if (timeoutMs === undefined) return await task;
      if (timeoutMs <= 0) throw new SingleFlightRejected("waiter-timeout");
      return await Promise.race([
        task,
        new Promise<T>((_, reject) => {
          setTimeout(() => reject(new SingleFlightRejected("waiter-timeout")), timeoutMs);
        }),
      ]);
    } finally {
      const remaining = (this.waiters.get(key) ?? 1) - 1;
      if (remaining <= 0) this.waiters.delete(key);
      else this.waiters.set(key, remaining);
    }
  }

  snapshot(): Record<string, unknown> {
    return {
      fills: this.tasks.size,
      waiters: Object.fromEntries([...this.waiters.entries()].sort()),
      maxFills: this.maxConcurrentFills,
      maxWaitersPerKey: this.maxWaitersPerKey,
    };
  }
}
