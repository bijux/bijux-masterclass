export interface CallCounter {
  readonly count: () => number;
  readonly increment: () => number;
}

export function createCallCounter(): CallCounter {
  let calls = 0;
  return { count: () => calls, increment: () => ++calls };
}
