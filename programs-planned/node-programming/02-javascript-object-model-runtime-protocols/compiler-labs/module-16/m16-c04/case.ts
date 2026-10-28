const value: Iterable<number> = { *[Symbol.iterator]() { yield 'wrong'; } };
console.log(value);
