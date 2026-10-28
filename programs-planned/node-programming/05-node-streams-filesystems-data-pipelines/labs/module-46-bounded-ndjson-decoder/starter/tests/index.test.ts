import test from 'node:test';
import assert from 'node:assert/strict';
import { isRecord, parseJsonLine } from '../src/index.js';
test('parses object line', () => assert.deepEqual(parseJsonLine({ number: 2, text: '{"id":1}' }), { id: 1 }));
test('rejects arrays as records', () => assert.equal(isRecord([]), false));
