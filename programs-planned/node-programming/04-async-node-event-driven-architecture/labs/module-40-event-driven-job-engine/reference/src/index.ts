export interface Job<T> {
  readonly id: string;
  readonly dependsOn: readonly string[];
  readonly run: (signal: AbortSignal) => Promise<T>;
}
export type JobEvent =
  | { readonly type: 'started'; readonly id: string }
  | { readonly type: 'succeeded'; readonly id: string }
  | { readonly type: 'failed'; readonly id: string; readonly error: unknown }
  | { readonly type: 'blocked'; readonly id: string }
  | { readonly type: 'cancelled'; readonly id: string };
export type JobOutcome<T> =
  | { readonly id: string; readonly status: 'succeeded'; readonly value: T }
  | { readonly id: string; readonly status: 'failed'; readonly error: unknown }
  | { readonly id: string; readonly status: 'blocked'; readonly blockedBy: readonly string[] }
  | { readonly id: string; readonly status: 'cancelled'; readonly reason: unknown };

function validate<T>(jobs: readonly Job<T>[]): Map<string, number> {
  const positions = new Map<string, number>();
  jobs.forEach((job, index) => {
    if (positions.has(job.id)) throw new Error(`duplicate job id: ${job.id}`);
    positions.set(job.id, index);
  });
  for (const job of jobs) for (const dependency of job.dependsOn) {
    if (!positions.has(dependency)) throw new Error(`unknown dependency: ${dependency}`);
    if (dependency === job.id) throw new Error(`self dependency: ${job.id}`);
  }
  const visiting = new Set<string>(); const visited = new Set<string>();
  const byId = new Map(jobs.map(job => [job.id, job] as const));
  function visit(id: string): void {
    if (visiting.has(id)) throw new Error(`cycle includes ${id}`);
    if (visited.has(id)) return;
    visiting.add(id);
    for (const dependency of byId.get(id)!.dependsOn) visit(dependency);
    visiting.delete(id); visited.add(id);
  }
  for (const job of jobs) visit(job.id);
  return positions;
}

export async function runJobEngine<T>(
  jobs: readonly Job<T>[],
  options: { readonly concurrency: number; readonly signal?: AbortSignal; readonly onEvent?: (event: JobEvent) => void },
): Promise<readonly JobOutcome<T>[]> {
  if (!Number.isInteger(options.concurrency) || options.concurrency <= 0) throw new RangeError('invalid concurrency');
  const positions = validate(jobs);
  const outcomes: Array<JobOutcome<T> | undefined> = Array.from({ length: jobs.length }, () => undefined);
  const running = new Map<number, Promise<{ index: number; outcome: JobOutcome<T> }>>();
  const controller = new AbortController();
  const forward = (): void => controller.abort(options.signal?.reason);
  if (options.signal?.aborted) forward(); else options.signal?.addEventListener('abort', forward, { once: true });
  const emit = (event: JobEvent): void => { options.onEvent?.(event); };
  try {
    while (outcomes.some(outcome => outcome === undefined)) {
      let changed = false;
      for (let index = 0; index < jobs.length; index += 1) {
        if (outcomes[index] || running.has(index)) continue;
        const job = jobs[index]!;
        const dependencyOutcomes = job.dependsOn.map(id => outcomes[positions.get(id)!]);
        const blockedBy = job.dependsOn.filter((_, depIndex) => {
          const outcome = dependencyOutcomes[depIndex];
          return outcome !== undefined && outcome.status !== 'succeeded';
        });
        if (blockedBy.length > 0) {
          outcomes[index] = { id: job.id, status: 'blocked', blockedBy };
          emit({ type: 'blocked', id: job.id }); changed = true; continue;
        }
        if (!dependencyOutcomes.every(outcome => outcome?.status === 'succeeded')) continue;
        if (controller.signal.aborted) {
          outcomes[index] = { id: job.id, status: 'cancelled', reason: controller.signal.reason };
          emit({ type: 'cancelled', id: job.id }); changed = true; continue;
        }
        if (running.size >= options.concurrency) continue;
        emit({ type: 'started', id: job.id });
        const promise = Promise.resolve().then(() => job.run(controller.signal)).then<JobOutcome<T>, JobOutcome<T>>(
          value => ({ id: job.id, status: 'succeeded', value }),
          error => controller.signal.aborted
            ? ({ id: job.id, status: 'cancelled', reason: controller.signal.reason })
            : ({ id: job.id, status: 'failed', error }),
        ).then(outcome => ({ index, outcome }));
        running.set(index, promise); changed = true;
      }
      if (running.size > 0) {
        const completed = await Promise.race(running.values());
        running.delete(completed.index);
        outcomes[completed.index] = completed.outcome;
        emit(completed.outcome.status === 'succeeded'
          ? { type: 'succeeded', id: completed.outcome.id }
          : completed.outcome.status === 'failed'
            ? { type: 'failed', id: completed.outcome.id, error: completed.outcome.error }
            : { type: 'cancelled', id: completed.outcome.id });
        continue;
      }
      if (!changed) throw new Error('scheduler made no progress');
    }
    return outcomes as readonly JobOutcome<T>[];
  } finally {
    options.signal?.removeEventListener('abort', forward);
  }
}
