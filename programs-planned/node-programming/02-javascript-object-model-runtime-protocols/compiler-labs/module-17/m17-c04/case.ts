function* values(): Generator<number,void,void> { yield 'wrong'; }
console.log(values());
