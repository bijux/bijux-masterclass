const iterator: Iterator<number> = { next() { return { done: false, value: 'x' }; } };
console.log(iterator);
