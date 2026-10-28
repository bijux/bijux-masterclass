interface Store { load(): Promise<readonly string[]>; save(values: readonly string[]): Promise<void> }
const fake: Store = {
  load: async () => ['a'],
  save: async (_values) => {},
};
console.log((await fake.load()).length);
