import test from 'node:test';
import assert from 'node:assert/strict';
import { calibratedCelsius, toFahrenheit, type Reading } from '../src/index.js';

test('public API composes conversion', () => {
  const reading: Reading = calibratedCelsius(10, 'lab');
  assert.equal(reading.celsius, 10.2);
  assert.equal(toFahrenheit({ celsius: 0, profile: 'field' }), 32);
});

test('private map cannot be mutated through returned data', () => {
  const first = calibratedCelsius(0, 'lab');
  const second = calibratedCelsius(0, 'lab');
  assert.deepEqual(first, second);
  assert.notEqual(first, second);
});
