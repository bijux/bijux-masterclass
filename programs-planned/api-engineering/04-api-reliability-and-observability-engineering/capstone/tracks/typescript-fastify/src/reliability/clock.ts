export interface Clock { nowMs(): number }

export class ManualClock implements Clock {
  public constructor(private current: number = 0) {}
  public nowMs(): number { return this.current; }
  public advance(milliseconds: number): void {
    if (!Number.isSafeInteger(milliseconds) || milliseconds < 0) throw new Error("clock cannot move backwards");
    this.current += milliseconds;
  }
}

export class SystemClock implements Clock {
  public nowMs(): number { return Date.now(); }
}
