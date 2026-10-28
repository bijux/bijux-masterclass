const state = { kind: 'ready', count: 1 } satisfies { kind: 'ready' | 'closed'; count: number };
const ready: 'ready' = state.kind;
console.log(ready);
