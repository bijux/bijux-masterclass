const factory = (value: number) => ({ value });
const instance = new factory(1);
console.log(instance);
