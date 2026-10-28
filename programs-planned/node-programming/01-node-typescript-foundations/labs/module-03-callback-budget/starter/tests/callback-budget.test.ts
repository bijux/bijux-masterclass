import test from 'node:test';
import assert from 'node:assert/strict';
import { createCallCounter } from '../src/index.js';

test('counter captures one private binding', () => {
  const counter = createCallCounter();
  assert.equal(counter.increment(), 1);
  assert.equal(counter.increment(), 2);
  assert.equal(counter.count(), 2);
});
