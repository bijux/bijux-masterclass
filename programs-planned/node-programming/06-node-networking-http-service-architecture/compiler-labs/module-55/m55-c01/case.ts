export interface Route<I,O> { readonly parse:(value:unknown)=>I; readonly handle:(input:I)=>O }
export const route: Route<number,string> = { parse: Number, handle: String };
