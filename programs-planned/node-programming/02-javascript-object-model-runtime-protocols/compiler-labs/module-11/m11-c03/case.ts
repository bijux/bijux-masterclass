const hidden = Symbol('hidden');
const value = { visible: 1, [hidden]: 2 };
const keys: readonly PropertyKey[] = Reflect.ownKeys(value);
console.log(keys.length);
