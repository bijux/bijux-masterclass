const target = {};
Object.defineProperty(target, 'fixed', { value: 1, configurable: false });
console.log(Reflect.ownKeys(new Proxy(target, { ownKeys: () => [] })));
