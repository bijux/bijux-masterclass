export type BasicTrace = readonly ['synchronous-start', 'synchronous-end'];

export function synchronousTrace(): BasicTrace {
  return ['synchronous-start', 'synchronous-end'];
}

export function mapSynchronously<T, U>(
  values: readonly T[],
  transform: (value: T, index: number) => U,
): readonly U[] {
  return values.map(transform);
}
