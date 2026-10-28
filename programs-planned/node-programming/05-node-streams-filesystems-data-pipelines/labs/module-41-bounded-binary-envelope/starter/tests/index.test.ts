import test from 'node:test';
import assert from 'node:assert/strict';
import { copyVisibleBytes, readHeader } from '../src/index.js';
test('copies only the visible range', () => { const backing = Buffer.from([9, 1, 2, 8]); const out = copyVisibleBytes(backing.subarray(1, 3)); backing[1] = 7; assert.deepEqual([...out], [1, 2]); });
test('returns no header for short input', () => assert.equal(readHeader(Buffer.alloc(6)), undefined));
