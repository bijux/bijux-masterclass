import test from 'node:test';
import assert from 'node:assert/strict';
import { FixedTime } from '../src/index.js';

test('starter exposes an injected time source', () => {
  const time = new FixedTime(10);
  assert.equal(time.now(), 10); time.set(20); assert.equal(time.now(), 20);
});
