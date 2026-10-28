export async function* fromValues<T>(values: readonly T[]): AsyncGenerator<T> {
  for (const value of values) yield value;
}
