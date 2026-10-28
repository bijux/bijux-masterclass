import test from 'node:test';
import assert from 'node:assert/strict';
import { titles } from '../src/index.js';

test('projects titles in source order', () => {
  assert.deepEqual(titles([{ id: 2, title: 'B' }, { id: 1, title: 'A' }]), ['B', 'A']);
});
