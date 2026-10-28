const value = { [Symbol.toPrimitive]() { return {}; } };
console.log(String(value));
