class Value { [Symbol.toPrimitive](): string | number { return {}; } }
console.log(new Value());
