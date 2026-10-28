const value = {};
Object.defineProperty(value, 'danger', { enumerable: true, get() { throw new Error('getter executed'); } });
console.log({ ...value });
