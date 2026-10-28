import test from 'node:test';
import assert from 'node:assert/strict';
import { isSupportedMajor } from '../src/index.js';

test('recognizes the course baseline', () => {
  assert.equal(isSupportedMajor(24), true);
  assert.equal(isSupportedMajor(23), false);
});
