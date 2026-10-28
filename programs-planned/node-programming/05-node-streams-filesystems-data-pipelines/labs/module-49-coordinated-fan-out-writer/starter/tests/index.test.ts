import test from 'node:test';
import assert from 'node:assert/strict';
import { assertConservation } from '../src/index.js';
test('accepts complete accounting', () => assert.doesNotThrow(() => assertConservation({ inspected: 3, emitted: 1, filtered: 1, rejected: 1 })));
test('rejects missing terminal outcome', () => assert.throws(() => assertConservation({ inspected: 3, emitted: 1, filtered: 1, rejected: 0 })));
