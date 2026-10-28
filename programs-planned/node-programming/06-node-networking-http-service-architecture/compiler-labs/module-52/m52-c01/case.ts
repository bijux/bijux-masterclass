export type State = { readonly kind: 'prefix'; readonly bytes: number } | { readonly kind: 'payload'; readonly expected: number };
export function remaining(state: State): number { switch (state.kind) { case 'prefix': return 4 - state.bytes; case 'payload': return state.expected; } }
