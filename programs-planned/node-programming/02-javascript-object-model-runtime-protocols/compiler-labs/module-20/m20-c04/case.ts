type Representation = { kind: 'live' } | { kind: 'record' } | { kind: 'debug' };
function assertNever(value: never): never { throw new Error(String(value)); }
function label(value: Representation): string { switch (value.kind) { case 'live': return 'live'; case 'record': return 'record'; default: return assertNever(value); } }
console.log(label({ kind: 'debug' }));
