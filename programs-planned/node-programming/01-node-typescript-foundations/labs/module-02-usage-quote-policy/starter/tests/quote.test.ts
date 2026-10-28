import test from 'node:test';
import assert from 'node:assert/strict';
import { formatCents, isPlan } from '../src/index.js';

test('recognizes plans and renders cents', () => {
  assert.equal(isPlan('team'), true);
  assert.equal(isPlan('other'), false);
  assert.equal(formatCents(205), '$2.05');
});
