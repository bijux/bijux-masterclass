export class DeadlineExceededError extends Error {
  constructor() { super('deadline exceeded'); this.name = 'DeadlineExceededError'; }
}

export class Budget {
  constructor(
    readonly deadline: number,
    private readonly nowSource: () => number = () => performance.now(),
  ) {}
  now(): number { return this.nowSource(); }
  remaining(): number { return Math.max(0, this.deadline - this.now()); }
  child(maximumMilliseconds: number): Budget {
    if (!Number.isFinite(maximumMilliseconds) || maximumMilliseconds < 0) {
      throw new RangeError('maximumMilliseconds must be finite and non-negative');
    }
    return new Budget(Math.min(this.deadline, this.now() + maximumMilliseconds), this.nowSource);
  }
}

function linkAbort(parent: AbortSignal | undefined, target: AbortController): () => void {
  if (!parent) return () => undefined;
  const forward = (): void => target.abort(parent.reason);
  if (parent.aborted) forward();
  else parent.addEventListener('abort', forward, { once: true });
  return () => parent.removeEventListener('abort', forward);
}

export async function withinBudget<T>(
  budget: Budget,
  operation: (signal: AbortSignal) => Promise<T>,
  parent?: AbortSignal,
): Promise<T> {
  const remaining = budget.remaining();
  if (remaining <= 0) throw new DeadlineExceededError();
  const controller = new AbortController();
  const unlink = linkAbort(parent, controller);
  const timer = setTimeout(() => controller.abort(new DeadlineExceededError()), remaining);
  try {
    controller.signal.throwIfAborted();
    return await operation(controller.signal);
  } catch (error) {
    if (controller.signal.aborted && controller.signal.reason instanceof DeadlineExceededError) {
      throw controller.signal.reason;
    }
    throw error;
  } finally {
    clearTimeout(timer);
    unlink();
  }
}

export function abortableDelay(milliseconds: number, signal: AbortSignal): Promise<void> {
  if (signal.aborted) return Promise.reject(signal.reason);
  return new Promise<void>((resolve, reject) => {
    const timer = setTimeout(() => {
      signal.removeEventListener('abort', onAbort);
      resolve();
    }, milliseconds);
    const onAbort = (): void => {
      clearTimeout(timer);
      signal.removeEventListener('abort', onAbort);
      reject(signal.reason);
    };
    signal.addEventListener('abort', onAbort, { once: true });
  });
}
