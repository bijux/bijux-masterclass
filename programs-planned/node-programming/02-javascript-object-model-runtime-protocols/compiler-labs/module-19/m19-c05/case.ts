const source: { self?: unknown } = {};
source.self = source;
const copy = structuredClone(source);
console.log(copy !== source && copy.self === copy);
