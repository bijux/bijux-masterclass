let revision = 0;
function* values() { const expected = revision; yield 1; if (expected !== revision) throw new Error('traversal invalidated'); yield 2; }
const iterator = values();
iterator.next(); revision += 1; iterator.next();
