interface View { readonly id: string; readonly children: readonly string[] }
const view: View = { id: 'a', children: ['b'] };
console.log(view.children.length);
