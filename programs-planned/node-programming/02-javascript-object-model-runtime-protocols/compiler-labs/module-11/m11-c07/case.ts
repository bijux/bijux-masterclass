const metadata: unique symbol = Symbol('metadata');
interface Value { readonly [metadata]: number }
const value: Value = { [metadata]: 3 };
console.log(value[metadata]);
