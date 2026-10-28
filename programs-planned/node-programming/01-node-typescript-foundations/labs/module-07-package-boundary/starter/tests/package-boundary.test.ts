import test from 'node:test';
import assert from 'node:assert/strict';
import { fromCelsius } from '../src/public.js';

test('public entry creates readings', () => assert.deepEqual(fromCelsius(3), { celsius: 3 }));
