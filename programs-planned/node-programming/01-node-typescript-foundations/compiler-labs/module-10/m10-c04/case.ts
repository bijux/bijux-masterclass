import assert from 'node:assert/strict';
const before = { count: 1 };
const after = before;
after.count += 1;
assert.equal(before.count, 1, 'prior value must remain unchanged');
