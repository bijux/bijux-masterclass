export async function collect<T>(source: AsyncIterable<T>): Promise<T[]> { const out: T[] = []; for await (const item of source)
    out.push(item); return out; }
export async function* fromValues<T>(values: readonly T[]): AsyncGenerator<T> { for (const value of values)
    yield value; }
