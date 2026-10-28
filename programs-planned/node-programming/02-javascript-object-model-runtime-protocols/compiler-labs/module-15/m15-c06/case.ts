const behavior = {};
Object.defineProperty(behavior, 'danger', { enumerable: true, get() { throw new Error('mixin getter executed'); } });
console.log(Object.assign({}, behavior));
