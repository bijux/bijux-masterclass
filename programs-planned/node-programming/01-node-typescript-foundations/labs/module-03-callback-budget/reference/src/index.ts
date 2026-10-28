export interface CallCounter {
  readonly count: () => number;
  readonly increment: () => number;
}

export function createCallCounter(): CallCounter {
  let calls = 0;
  return { count: () => calls, increment: () => ++calls };
}

export type SearchResult<Result> =
  | { readonly kind: 'accepted'; readonly value: Result; readonly sourceIndex: number; readonly calls: number }
  | { readonly kind: 'source-exhausted'; readonly calls: number }
  | { readonly kind: 'budget-exhausted'; readonly calls: number };

export function firstAccepted<Input, Result>(
  values: readonly Input[],
  maxCalls: number,
  attempt: (value: Input, sourceIndex: number) => Result,
  accept: (result: Result) => boolean,
): SearchResult<Result> {
  if (!Number.isSafeInteger(maxCalls) || maxCalls < 0) throw new Error('maxCalls must be a nonnegative safe integer');
  let calls = 0;
  for (let index = 0; index < values.length; index += 1) {
    if (calls === maxCalls) return { kind: 'budget-exhausted', calls };
    const value = values[index];
    if (value === undefined) throw new Error('index invariant failed');
    const result = attempt(value, index);
    calls += 1;
    if (accept(result)) return { kind: 'accepted', value: result, sourceIndex: index, calls };
  }
  return { kind: 'source-exhausted', calls };
}
