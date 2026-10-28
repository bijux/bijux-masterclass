const value = {};
const descriptor = Object.getOwnPropertyDescriptor(value, 'missing');
console.log(descriptor.enumerable);
