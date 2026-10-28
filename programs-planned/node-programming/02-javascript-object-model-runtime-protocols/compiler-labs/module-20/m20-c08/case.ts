function isIterable(value: unknown): value is Iterable<unknown> { return typeof value === 'object' && value !== null && typeof Reflect.get(value, Symbol.iterator) === 'function'; }
const value: unknown = [1, 2];
if (isIterable(value)) console.log([...value].length);
