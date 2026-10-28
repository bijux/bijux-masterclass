const registry = new FinalizationRegistry<string>((label) => console.log(label));
const value = {};
registry.register(value, 'optional diagnostic');
console.log(typeof value);
