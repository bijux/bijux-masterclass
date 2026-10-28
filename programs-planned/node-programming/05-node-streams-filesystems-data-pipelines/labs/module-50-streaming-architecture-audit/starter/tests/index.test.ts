import test from 'node:test';
import assert from 'node:assert/strict';
import { missingFields } from '../src/index.js';
test('reports incomplete stage contract', () => assert.deepEqual(missingFields({ name: 'source' }), ['input', 'output', 'owner', 'bound', 'completion']));
