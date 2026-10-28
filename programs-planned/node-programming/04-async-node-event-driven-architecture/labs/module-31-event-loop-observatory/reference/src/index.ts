export type TraceLabel =
  | 'synchronous-start'
  | 'timer-callback'
  | 'next-tick'
  | 'queue-microtask'
  | 'promise-reaction'
  | 'immediate-after-timer';

export async function observeControlledTurn(): Promise<readonly TraceLabel[]> {
  const trace: TraceLabel[] = ['synchronous-start'];
  await new Promise<void>(resolve => {
    setTimeout(() => {
      trace.push('timer-callback');
      process.nextTick(() => trace.push('next-tick'));
      queueMicrotask(() => trace.push('queue-microtask'));
      Promise.resolve().then(() => trace.push('promise-reaction'));
      setImmediate(() => {
        trace.push('immediate-after-timer');
        resolve();
      });
    }, 0);
  });
  return trace;
}

function yieldToCheck(signal?: AbortSignal): Promise<void> {
  if (signal?.aborted) return Promise.reject(signal.reason);
  return new Promise<void>((resolve, reject) => {
    const handle = setImmediate(() => {
      signal?.removeEventListener('abort', onAbort);
      resolve();
    });
    const onAbort = (): void => {
      clearImmediate(handle);
      signal?.removeEventListener('abort', onAbort);
      reject(signal?.reason);
    };
    signal?.addEventListener('abort', onAbort, { once: true });
  });
}

export async function cooperativeMap<T, U>(
  values: readonly T[],
  chunkSize: number,
  transform: (value: T, index: number) => U,
  signal?: AbortSignal,
): Promise<readonly U[]> {
  if (!Number.isInteger(chunkSize) || chunkSize <= 0) {
    throw new RangeError('chunkSize must be a positive integer');
  }
  const output: U[] = [];
  for (let start = 0; start < values.length; start += chunkSize) {
    signal?.throwIfAborted();
    const end = Math.min(start + chunkSize, values.length);
    for (let index = start; index < end; index += 1) {
      output.push(transform(values[index]!, index));
    }
    if (end < values.length) await yieldToCheck(signal);
  }
  return output;
}
