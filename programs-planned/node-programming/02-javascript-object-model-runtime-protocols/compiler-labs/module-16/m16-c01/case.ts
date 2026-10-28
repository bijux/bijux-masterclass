const protocol: unique symbol = Symbol('protocol');
interface Value { [protocol](): string }
const value: Value = { [protocol]: () => 'ok' };
console.log(value[protocol]());
