interface Item { readonly id: number; readonly tags: readonly string[] }
const item: Item = { id: 1, tags: ['node'] };
console.log(item.tags[0]);
