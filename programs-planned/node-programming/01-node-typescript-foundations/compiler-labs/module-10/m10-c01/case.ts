interface Clock { readonly now: () => Date }
function stamp(clock: Clock): string { return clock.now().toISOString(); }
console.log(stamp({ now: () => new Date('2026-01-01T00:00:00.000Z') }));
