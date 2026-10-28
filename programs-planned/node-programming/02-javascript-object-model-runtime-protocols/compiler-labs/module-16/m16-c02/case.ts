const left: unique symbol = Symbol('x');
const right: unique symbol = Symbol('x');
const value: typeof left = right;
console.log(value);
