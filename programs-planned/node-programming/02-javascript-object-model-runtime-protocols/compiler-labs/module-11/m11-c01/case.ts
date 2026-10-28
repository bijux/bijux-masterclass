const target: object = {};
Object.defineProperty(target, 'id', { value: 'n1', writable: false, enumerable: true, configurable: false });
const descriptor = Object.getOwnPropertyDescriptor(target, 'id');
if (descriptor === undefined || descriptor.writable !== false) throw new Error('descriptor');
