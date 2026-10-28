interface Clock { now(): string }
function stamp(clock: Clock): string { return clock.now(); }
console.log(stamp({ now: () => 't' }));
