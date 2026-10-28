const value: Iterable<number> = { *[Symbol.iterator]() { yield 1; yield 2; } };
console.log([...value].length);
