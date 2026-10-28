type Line = { readonly kind: 'line'; readonly value: string } | { readonly kind: 'error'; readonly message: string };
const value: Line = { kind: 'line', value: 'ok' };
void value;
