class Value { get [Symbol.toStringTag](): string { return 'Value'; } }
console.log(Object.prototype.toString.call(new Value()));
