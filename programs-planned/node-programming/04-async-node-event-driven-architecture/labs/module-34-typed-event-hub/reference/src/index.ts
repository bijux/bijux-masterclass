import { EventEmitter } from 'node:events';

type EventKey<E> = Extract<keyof E, string | symbol>;
type Listener<Args extends readonly unknown[]> = (...args: Args) => void;

export class TypedEventHub<Events extends { [K in keyof Events]: readonly unknown[] }> {
  #emitter = new EventEmitter();

  on<K extends EventKey<Events>>(event: K, listener: Listener<Events[K]>): () => void {
    this.#emitter.on(event, listener);
    let active = true;
    return () => {
      if (!active) return;
      active = false;
      this.#emitter.off(event, listener);
    };
  }

  once<K extends EventKey<Events>>(event: K, signal?: AbortSignal): Promise<Events[K]> {
    if (signal?.aborted) return Promise.reject(signal.reason);
    return new Promise<Events[K]>((resolve, reject) => {
      const cleanup = (): void => {
        this.#emitter.off(event, onEvent);
        signal?.removeEventListener('abort', onAbort);
      };
      const onEvent = (...args: Events[K]): void => { cleanup(); resolve(args); };
      const onAbort = (): void => { cleanup(); reject(signal?.reason); };
      this.#emitter.once(event, onEvent);
      signal?.addEventListener('abort', onAbort, { once: true });
    });
  }

  emit<K extends EventKey<Events>>(event: K, ...args: Events[K]): boolean {
    return this.#emitter.emit(event, ...args);
  }

  listenerCount<K extends EventKey<Events>>(event: K): number {
    return this.#emitter.listenerCount(event);
  }
}
