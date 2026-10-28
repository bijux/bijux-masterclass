import test from 'node:test';
import assert from 'node:assert/strict';
import { totalStock } from '../src/index.js';

test('summarizes stock without mutation', () => {
  const inventory = { items: [{ id: 1, name: 'paper', stock: 3 }] };
  assert.equal(totalStock(inventory), 3);
});
