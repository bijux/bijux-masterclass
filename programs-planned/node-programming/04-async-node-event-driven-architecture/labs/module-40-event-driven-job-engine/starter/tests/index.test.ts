import test from 'node:test';
import assert from 'node:assert/strict';
import { validateReferences } from '../src/index.js';

test('starter validates duplicate and unknown references', () => {
  validateReferences([{ id: 'a', dependsOn: [] }, { id: 'b', dependsOn: ['a'] }]);
  assert.throws(() => validateReferences([{ id: 'a', dependsOn: ['x'] }]), /unknown/);
});
