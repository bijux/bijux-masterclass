import test from 'node:test';
import assert from 'node:assert/strict';
import { CallbackSet } from '../src/index.js';

test('starter subscription can be removed', () => {
  const callbacks = new CallbackSet<number>();
  const seen: number[] = [];
  const off = callbacks.on(value => seen.push(value));
  callbacks.emit(1); off(); callbacks.emit(2);
  assert.deepEqual(seen, [1]);
});
