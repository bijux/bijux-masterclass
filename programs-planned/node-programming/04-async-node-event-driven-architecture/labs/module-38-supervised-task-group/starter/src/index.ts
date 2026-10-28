export interface SequentialJob<T> { readonly id: string; readonly run: () => Promise<T>; }
export async function runSequential<T>(jobs: readonly SequentialJob<T>[]): Promise<readonly T[]> {
  const output: T[] = [];
  for (const job of jobs) output.push(await job.run());
  return output;
}
