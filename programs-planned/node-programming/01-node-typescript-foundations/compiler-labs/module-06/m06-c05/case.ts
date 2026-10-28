const source: readonly number[] = [3, 1, 2];
const sorted = [...source].sort((a, b) => a - b);
console.log(source.join(','), sorted.join(','));
