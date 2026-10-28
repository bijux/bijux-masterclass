const target = {};
const proxy = new Proxy(target, { defineProperty(t,key,descriptor) { return Reflect.defineProperty(t,key,descriptor); } });
Object.defineProperty(proxy, 'x', { value: 1 });
console.log(Reflect.get(target,'x'));
