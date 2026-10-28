interface Consumer<T> {
  readonly resolve: (result: IteratorResult<T>) => void;
  readonly reject: (reason: unknown) => void;
}
interface Producer<T> {
  readonly value: T;
  readonly resolve: () => void;
  readonly reject: (reason: unknown) => void;
  readonly signal: AbortSignal | undefined;
  readonly onAbort: (() => void) | undefined;
}

export class BoundedAsyncQueue<T> implements AsyncIterable<T> {
  #buffer: T[] = [];
  #consumers: Consumer<T>[] = [];
  #producers: Producer<T>[] = [];
  #closed = false;
  #failure: unknown | undefined;
  #claimed = false;

  constructor(readonly capacity: number) {
    if (!Number.isInteger(capacity) || capacity <= 0) throw new RangeError('capacity must be positive');
  }

  get size(): number { return this.#buffer.length; }

  async push(value: T, signal?: AbortSignal): Promise<void> {
    if (signal?.aborted) throw signal.reason;
    if (this.#failure !== undefined) throw this.#failure;
    if (this.#closed) throw new Error('queue is closed');
    const consumer = this.#consumers.shift();
    if (consumer) { consumer.resolve({ done: false, value }); return; }
    if (this.#buffer.length < this.capacity) { this.#buffer.push(value); return; }
    await new Promise<void>((resolve, reject) => {
      let producer: Producer<T>;
      const activeSignal = signal;
      let onAbort: (() => void) | undefined;
      if (activeSignal) {
        const listener = (): void => {
          this.#producers = this.#producers.filter(item => item !== producer);
          activeSignal.removeEventListener('abort', listener);
          reject(activeSignal.reason);
        };
        onAbort = listener;
        activeSignal.addEventListener('abort', listener, { once: true });
      }
      producer = { value, resolve, reject, signal, onAbort };
      this.#producers.push(producer);
    });
  }

  close(): void {
    if (this.#closed || this.#failure !== undefined) return;
    this.#closed = true;
    for (const producer of this.#producers.splice(0)) {
      if (producer.onAbort && producer.signal) producer.signal.removeEventListener('abort', producer.onAbort);
      producer.reject(new Error('queue is closed'));
    }
    this.#finishConsumersIfDrained();
  }

  fail(reason: unknown): void {
    if (this.#closed || this.#failure !== undefined) return;
    this.#failure = reason;
    this.#buffer = [];
    for (const producer of this.#producers.splice(0)) {
      if (producer.onAbort && producer.signal) producer.signal.removeEventListener('abort', producer.onAbort);
      producer.reject(reason);
    }
    for (const consumer of this.#consumers.splice(0)) consumer.reject(reason);
  }

  async take(): Promise<IteratorResult<T>> {
    if (this.#buffer.length > 0) {
      const value = this.#buffer.shift()!;
      this.#admitProducer();
      this.#finishConsumersIfDrained();
      return { done: false, value };
    }
    if (this.#failure !== undefined) throw this.#failure;
    if (this.#closed) return { done: true, value: undefined };
    return new Promise<IteratorResult<T>>((resolve, reject) => this.#consumers.push({ resolve, reject }));
  }

  [Symbol.asyncIterator](): AsyncIterator<T> {
    if (this.#claimed) throw new Error('queue supports one consumer');
    this.#claimed = true;
    return {
      next: () => this.take(),
      return: async () => {
        this.fail(new Error('consumer ended iteration'));
        return { done: true, value: undefined };
      },
    };
  }

  #admitProducer(): void {
    const producer = this.#producers.shift();
    if (!producer) return;
    if (producer.onAbort && producer.signal) producer.signal.removeEventListener('abort', producer.onAbort);
    const consumer = this.#consumers.shift();
    if (consumer) consumer.resolve({ done: false, value: producer.value });
    else this.#buffer.push(producer.value);
    producer.resolve();
  }

  #finishConsumersIfDrained(): void {
    if (!this.#closed || this.#buffer.length > 0) return;
    for (const consumer of this.#consumers.splice(0)) consumer.resolve({ done: true, value: undefined });
  }
}
