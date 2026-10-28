interface Route<I,O> { readonly handle:(input:I)=>O }
export const route: Route<number,string> = { handle: (value) => value + 1 };
