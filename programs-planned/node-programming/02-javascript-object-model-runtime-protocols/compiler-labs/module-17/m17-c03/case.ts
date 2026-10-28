function* values(): Generator<number,string,void> { yield 1; return 'done'; }
const iterator = values();
console.log(iterator.next().value);
