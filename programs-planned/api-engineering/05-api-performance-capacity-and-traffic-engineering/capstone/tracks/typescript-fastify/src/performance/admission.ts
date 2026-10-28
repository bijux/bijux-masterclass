export class AdmissionRejected extends Error {
  constructor(readonly reason: string) {
    super(reason);
  }
}

export interface AdmissionSnapshot {
  active: number;
  waiting: number;
  activeByKey: Record<string, number>;
  maxActive: number;
  maxWaiters: number;
}

interface Waiter {
  key: string;
  resolve: (permit: AdmissionPermit) => void;
  reject: (error: Error) => void;
  timer?: ReturnType<typeof setTimeout>;
  settled: boolean;
}

export class AdmissionPermit {
  private released = false;

  constructor(
    private readonly controller: FairAdmission,
    readonly key: string,
  ) {}

  release(): void {
    if (this.released) throw new Error("permit released twice");
    this.released = true;
    this.controller.releaseInternal(this.key);
  }
}

export class FairAdmission {
  private active = 0;
  private readonly activeByKey = new Map<string, number>();
  private readonly waiters: Waiter[] = [];

  constructor(
    readonly maxActive: number,
    readonly maxWaiters: number,
    readonly maxActivePerKey: number,
  ) {
    if (
      !Number.isSafeInteger(maxActive) ||
      !Number.isSafeInteger(maxWaiters) ||
      !Number.isSafeInteger(maxActivePerKey) ||
      maxActive <= 0 ||
      maxWaiters < 0 ||
      maxActivePerKey <= 0 ||
      maxActivePerKey > maxActive
    ) {
      throw new Error("invalid admission limits");
    }
  }

  private keyActive(key: string): number {
    return this.activeByKey.get(key) ?? 0;
  }

  private canGrant(key: string): boolean {
    return this.active < this.maxActive && this.keyActive(key) < this.maxActivePerKey;
  }

  acquire(key: string, timeoutMs?: number): Promise<AdmissionPermit> {
    if (!key) return Promise.reject(new Error("admission key is required"));
    if (this.waiters.length === 0 && this.canGrant(key)) {
      this.active += 1;
      this.activeByKey.set(key, this.keyActive(key) + 1);
      return Promise.resolve(new AdmissionPermit(this, key));
    }
    if (this.waiters.length >= this.maxWaiters) {
      return Promise.reject(new AdmissionRejected("waiter-capacity"));
    }
    if (timeoutMs !== undefined && timeoutMs <= 0) {
      return Promise.reject(new AdmissionRejected("admission-timeout"));
    }
    return new Promise<AdmissionPermit>((resolve, reject) => {
      const waiter: Waiter = { key, resolve, reject, settled: false };
      if (timeoutMs !== undefined) {
        waiter.timer = setTimeout(() => {
          if (waiter.settled) return;
          waiter.settled = true;
          const index = this.waiters.indexOf(waiter);
          if (index >= 0) this.waiters.splice(index, 1);
          reject(new AdmissionRejected("admission-timeout"));
          this.schedule();
        }, timeoutMs);
      }
      this.waiters.push(waiter);
      this.schedule();
    });
  }

  private schedule(): void {
    while (this.active < this.maxActive) {
      const index = this.waiters.findIndex(
        (waiter) => !waiter.settled && this.canGrant(waiter.key),
      );
      if (index < 0) return;
      const [waiter] = this.waiters.splice(index, 1);
      if (waiter === undefined || waiter.settled) continue;
      waiter.settled = true;
      if (waiter.timer !== undefined) clearTimeout(waiter.timer);
      this.active += 1;
      this.activeByKey.set(waiter.key, this.keyActive(waiter.key) + 1);
      waiter.resolve(new AdmissionPermit(this, waiter.key));
    }
  }

  releaseInternal(key: string): void {
    const count = this.keyActive(key);
    if (this.active <= 0 || count <= 0) throw new Error("admission state underflow");
    this.active -= 1;
    if (count === 1) this.activeByKey.delete(key);
    else this.activeByKey.set(key, count - 1);
    this.schedule();
  }

  snapshot(): AdmissionSnapshot {
    return {
      active: this.active,
      waiting: this.waiters.length,
      activeByKey: Object.fromEntries([...this.activeByKey.entries()].sort()),
      maxActive: this.maxActive,
      maxWaiters: this.maxWaiters,
    };
  }
}
