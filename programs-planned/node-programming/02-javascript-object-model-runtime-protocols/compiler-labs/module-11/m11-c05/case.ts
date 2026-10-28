const secret = Symbol('secret');
const value = {};
Object.defineProperty(value, 'hidden', { value: 1, enumerable: false });
Object.defineProperty(value, 'visible', { value: 2, enumerable: true });
Object.defineProperty(value, secret, { value: 3, enumerable: false });
console.log(`${Object.keys(value).join(',')}|${Reflect.ownKeys(value).length}`);
