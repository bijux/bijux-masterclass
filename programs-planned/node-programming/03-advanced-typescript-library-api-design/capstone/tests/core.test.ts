import assert from 'node:assert/strict';
import test from 'node:test';
import { SchemaError, boolean, literal, number, string } from '../src/index.js';

test('primitive schemas accept only their documented runtime domains', () => {
  assert.equal(string().parse('value'), 'value');
  assert.equal(boolean().parse(false), false);
  assert.equal(number().parse(2.5), 2.5);
  assert.equal(literal('V1').parse('V1'), 'V1');
  assert.throws(() => number().parse(Number.NaN), SchemaError);
  assert.throws(() => string().parse(42), /expected a string/);
});
