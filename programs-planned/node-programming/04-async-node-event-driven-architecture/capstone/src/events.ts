import { EventOverflowError } from './errors.js';

export type HarborEvent =
  | { readonly type: 'run-started'; readonly runId: string; readonly taskCount: number }
  | { readonly type: 'task-ready'; readonly runId: string; readonly taskId: string; readonly index: number }
  | { readonly type: 'task-started'; readonly runId: string; readonly taskId: string; readonly index: number }
  | { readonly type: 'task-succeeded'; readonly runId: string; readonly taskId: string; readonly index: number }
  | { readonly type: 'task-failed'; readonly runId: string; readonly taskId: string; readonly index: number; readonly error: unknown }
  | { readonly type: 'task-timed-out'; readonly runId: string; readonly taskId: string; readonly index: number; readonly error: unknown }
  | { readonly type: 'task-cancelled'; readonly runId: string; readonly taskId: string; readonly index: number; readonly reason: unknown }
  | { readonly type: 'task-blocked'; readonly runId: string; readonly taskId: string; readonly index: number; readonly blockedBy: readonly string[] }
  | { readonly type: 'run-finished'; readonly runId: string };

export class HarborEventHub {
  #listeners = new Set<(event: HarborEvent) => void>();
  on(listener: (event: HarborEvent) => void): () => void {
    this.#listeners.add(listener);
    let active = true;
    return () => { if (active) { active = false; this.#listeners.delete(listener); } };
  }
  emit(event: HarborEvent): readonly unknown[] {
    const errors: unknown[] = [];
    for (const listener of [...this.#listeners]) {
      try { listener(event); } catch (error) { errors.push(error); }
    }
    return errors;
  }
  get listenerCount(): number { return this.#listeners.size; }
}

class EventQueue implements AsyncIterable<HarborEvent> {
  #buffer: HarborEvent[] = [];
  #waiters: Array<{ resolve: (result: IteratorResult<HarborEvent>) => void; reject: (error: unknown) => void }> = [];
  #closed = false;
  #failure: unknown | undefined;
  constructor(private readonly capacity: number, private readonly dispose: () => void) {}
  push(event: HarborEvent): void {
    if (this.#closed || this.#failure !== undefined) return;
    const waiter = this.#waiters.shift();
    if (waiter) { waiter.resolve({ done: false, value: event }); return; }
    if (this.#buffer.length >= this.capacity) { this.fail(new EventOverflowError(this.capacity)); return; }
    this.#buffer.push(event);
  }
  close(): void {
    if (this.#closed || this.#failure !== undefined) return;
    this.#closed = true; this.dispose(); this.#finish();
  }
  fail(error: unknown): void {
    if (this.#closed || this.#failure !== undefined) return;
    this.#failure = error; this.dispose(); this.#buffer = [];
    for (const waiter of this.#waiters.splice(0)) waiter.reject(error);
  }
  #finish(): void {
    if (!this.#closed || this.#buffer.length > 0) return;
    for (const waiter of this.#waiters.splice(0)) waiter.resolve({ done: true, value: undefined });
  }
  async next(): Promise<IteratorResult<HarborEvent>> {
    if (this.#buffer.length > 0) { const value = this.#buffer.shift()!; this.#finish(); return { done: false, value }; }
    if (this.#failure !== undefined) throw this.#failure;
    if (this.#closed) return { done: true, value: undefined };
    return new Promise((resolve, reject) => this.#waiters.push({ resolve, reject }));
  }
  [Symbol.asyncIterator](): AsyncIterator<HarborEvent> {
    return { next: () => this.next(), return: async () => { this.close(); return { done: true, value: undefined }; } };
  }
}

export function eventStream(hub: HarborEventHub, options: { readonly capacity: number; readonly signal?: AbortSignal }): AsyncIterable<HarborEvent> {
  if (!Number.isInteger(options.capacity) || options.capacity <= 0) throw new RangeError('event capacity must be positive');
  let queue!: EventQueue;
  let unsubscribe = (): void => undefined;
  const onAbort = (): void => queue.fail(options.signal?.reason);
  const dispose = (): void => { unsubscribe(); options.signal?.removeEventListener('abort', onAbort); };
  queue = new EventQueue(options.capacity, dispose);
  unsubscribe = hub.on(event => queue.push(event));
  if (options.signal?.aborted) queue.fail(options.signal.reason);
  else options.signal?.addEventListener('abort', onAbort, { once: true });
  return queue;
}
