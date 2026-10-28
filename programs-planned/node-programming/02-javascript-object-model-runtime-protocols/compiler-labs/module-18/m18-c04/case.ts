interface Value { count: number }
const proxy: Value = new Proxy<Value>({ count: 1 }, { set(target,key,value,receiver) { return Reflect.set(target,key,value,receiver); } });
console.log(proxy.count);
