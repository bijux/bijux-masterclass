type Constructor<Args extends readonly unknown[], Value> = new (...args: Args) => Value;
class Box { constructor(readonly value: number) {} }
const ctor: Constructor<[number], Box> = Box;
console.log(new ctor(2).value);
