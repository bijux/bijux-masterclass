export interface Clock {
  now(): number;
  sleep(milliseconds: number, signal?: AbortSignal): Promise<void>;
}

interface Sleeper {
  readonly id: number;
  readonly deadline: number;
  readonly resolve: () => void;
  readonly reject: (reason: unknown) => void;
  readonly signal: AbortSignal | undefined;
  readonly onAbort: (() => void) | undefined;
}

export class ManualClock implements Clock {
  #now = 0;
  #nextId = 0;
  #sleepers: Sleeper[] = [];
  now(): number { return this.#now; }
  pending(): number { return this.#sleepers.length; }

  sleep(milliseconds: number, signal?: AbortSignal): Promise<void> {
    if (!Number.isFinite(milliseconds) || milliseconds < 0) {
      return Promise.reject(new RangeError('milliseconds must be finite and non-negative'));
    }
    if (signal?.aborted) return Promise.reject(signal.reason);
    return new Promise<void>((resolve, reject) => {
      const id = this.#nextId++;
      const activeSignal = signal;
      let onAbort: (() => void) | undefined;
      if (activeSignal) {
        const listener = (): void => {
          this.#sleepers = this.#sleepers.filter(sleeper => sleeper.id !== id);
          activeSignal.removeEventListener('abort', listener);
          reject(activeSignal.reason);
        };
        onAbort = listener;
        activeSignal.addEventListener('abort', listener, { once: true });
      }
      this.#sleepers.push({ id, deadline: this.#now + milliseconds, resolve, reject, signal, onAbort });
      this.#sleepers.sort((a, b) => a.deadline - b.deadline || a.id - b.id);
    });
  }

  advanceBy(milliseconds: number): void {
    if (!Number.isFinite(milliseconds) || milliseconds < 0) throw new RangeError('invalid advance');
    this.#now += milliseconds;
    const due = this.#sleepers.filter(sleeper => sleeper.deadline <= this.#now);
    this.#sleepers = this.#sleepers.filter(sleeper => sleeper.deadline > this.#now);
    for (const sleeper of due) {
      if (sleeper.onAbort && sleeper.signal) sleeper.signal.removeEventListener('abort', sleeper.onAbort);
      sleeper.resolve();
    }
  }
}

export class PollDeadlineError extends Error {
  constructor() { super('poll deadline reached'); this.name = 'PollDeadlineError'; }
}

export async function pollUntil<T>(
  check: () => T | undefined,
  options: { readonly clock: Clock; readonly interval: number; readonly deadline: number; readonly signal?: AbortSignal },
): Promise<T> {
  if (options.interval <= 0) throw new RangeError('interval must be positive');
  while (true) {
    options.signal?.throwIfAborted();
    const value = check();
    if (value !== undefined) return value;
    const remaining = options.deadline - options.clock.now();
    if (remaining <= 0) throw new PollDeadlineError();
    await options.clock.sleep(Math.min(options.interval, remaining), options.signal);
  }
}
