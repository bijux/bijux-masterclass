const base = {};
Object.defineProperty(base, 'value', { get(this: { local: number }): number { return this.local; } });
const receiver = { local: 3 };
console.log(Reflect.get(base, 'value', receiver));
