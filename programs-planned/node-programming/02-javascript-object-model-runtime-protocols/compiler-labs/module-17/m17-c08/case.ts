function* values(): Generator<number> { yield 1; }
const iterator: IterableIterator<number> = values();
console.log([...iterator]);
