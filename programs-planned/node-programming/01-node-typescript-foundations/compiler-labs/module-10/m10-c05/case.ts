interface Store { save(text: string): Promise<void> }
const store: Store = {
  save: (_text: string) => undefined,
};
console.log(store);
