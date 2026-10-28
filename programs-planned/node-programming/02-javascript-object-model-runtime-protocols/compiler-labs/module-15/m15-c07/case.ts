interface Dependencies { readonly clock: { now(): string } }
const dependencies: Dependencies = { clock: { now: () => 'a' } };
dependencies.clock = { now: () => 'b' };
