export interface Clock {
  now(): number;
  sleep(milliseconds: number, signal?: AbortSignal): Promise<void>;
}

export class SystemClock implements Clock {
  now(): number { return performance.now(); }
  sleep(milliseconds: number, signal?: AbortSignal): Promise<void> {
    if (!Number.isFinite(milliseconds) || milliseconds < 0) return Promise.reject(new RangeError('invalid delay'));
    if (signal?.aborted) return Promise.reject(signal.reason);
    return new Promise<void>((resolve, reject) => {
      const timer = setTimeout(() => {
        signal?.removeEventListener('abort', onAbort);
        resolve();
      }, milliseconds);
      const onAbort = (): void => {
        clearTimeout(timer);
        signal?.removeEventListener('abort', onAbort);
        reject(signal?.reason);
      };
      signal?.addEventListener('abort', onAbort, { once: true });
    });
  }
}
