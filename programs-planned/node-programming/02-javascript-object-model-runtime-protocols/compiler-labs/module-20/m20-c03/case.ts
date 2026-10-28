type Representation = { kind: 'live'; value: object } | { kind: 'record'; value: Record<string, unknown> };
function label(value: Representation): string { switch (value.kind) { case 'live': return 'live'; case 'record': return 'record'; } }
console.log(label({ kind: 'record', value: {} }));
