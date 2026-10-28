import test from 'node:test';
import assert from 'node:assert/strict';
import { mapSynchronously, synchronousTrace } from '../src/index.js';

test('starter establishes synchronous order and source-order mapping', () => {
  assert.deepEqual(synchronousTrace(), ['synchronous-start', 'synchronous-end']);
  assert.deepEqual(mapSynchronously([3, 1, 2], value => value * 2), [6, 2, 4]);
});
