export interface TimeSource { now(): number; }
export class FixedTime implements TimeSource {
  constructor(private value: number) {}
  now(): number { return this.value; }
  set(value: number): void { this.value = value; }
}
