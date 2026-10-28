function sortInPlace(values: number[]): void { values.sort((a, b) => a - b); }
const source: readonly number[] = [3, 1, 2];
sortInPlace(source);
