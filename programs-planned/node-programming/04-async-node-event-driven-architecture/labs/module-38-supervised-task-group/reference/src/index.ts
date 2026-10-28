export interface SupervisedJob<T> {
  readonly id: string;
  readonly run: (signal: AbortSignal) => Promise<T>;
}
export type FailurePolicy = 'continue' | 'fail-fast';
export type SupervisedOutcome<T> =
  | { readonly id: string; readonly index: number; readonly status: 'succeeded'; readonly value: T }
  | { readonly id: string; readonly index: number; readonly status: 'failed'; readonly error: unknown }
  | { readonly id: string; readonly index: number; readonly status: 'cancelled'; readonly reason: unknown };

export async function runSupervised<T>(
  jobs: readonly SupervisedJob<T>[],
  options: { readonly concurrency: number; readonly policy: FailurePolicy; readonly signal?: AbortSignal },
): Promise<readonly SupervisedOutcome<T>[]> {
  if (!Number.isInteger(options.concurrency) || options.concurrency <= 0) throw new RangeError('invalid concurrency');
  const ids = new Set<string>();
  for (const job of jobs) {
    if (ids.has(job.id)) throw new Error(`duplicate job id: ${job.id}`);
    ids.add(job.id);
  }
  const controller = new AbortController();
  const forward = (): void => controller.abort(options.signal?.reason);
  if (options.signal?.aborted) forward();
  else options.signal?.addEventListener('abort', forward, { once: true });
  const outcomes: Array<SupervisedOutcome<T> | undefined> = Array(jobs.length);
  let next = 0;
  try {
    async function worker(): Promise<void> {
      while (true) {
        if (controller.signal.aborted && options.policy === 'fail-fast') return;
        const index = next++;
        if (index >= jobs.length) return;
        const job = jobs[index]!;
        if (controller.signal.aborted) {
          outcomes[index] = { id: job.id, index, status: 'cancelled', reason: controller.signal.reason };
          continue;
        }
        try {
          const value = await Promise.resolve().then(() => job.run(controller.signal));
          outcomes[index] = { id: job.id, index, status: 'succeeded', value };
        } catch (error) {
          if (controller.signal.aborted) {
            outcomes[index] = { id: job.id, index, status: 'cancelled', reason: controller.signal.reason };
          } else {
            outcomes[index] = { id: job.id, index, status: 'failed', error };
            if (options.policy === 'fail-fast') controller.abort(error);
          }
        }
      }
    }
    await Promise.all(Array.from({ length: Math.min(options.concurrency, jobs.length) }, () => worker()));
    for (let index = 0; index < jobs.length; index += 1) {
      if (!outcomes[index]) {
        const job = jobs[index]!;
        outcomes[index] = { id: job.id, index, status: 'cancelled', reason: controller.signal.reason };
      }
    }
    return outcomes as readonly SupervisedOutcome<T>[];
  } finally {
    options.signal?.removeEventListener('abort', forward);
  }
}
