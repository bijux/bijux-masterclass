import test from 'node:test';
import assert from 'node:assert/strict';
import { countChunks } from '../src/index.js';
test('counts bytes independently of chunking', () => { assert.deepEqual(countChunks([Buffer.from('a'), Buffer.from('bc')]), { chunks: 2, bytes: 3 }); });
