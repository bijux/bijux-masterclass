import test from 'node:test';
import assert from 'node:assert/strict';
import { collect, fromValues } from '../src/index.js';
test('collects a small bounded source', async () => assert.deepEqual(await collect(fromValues([1, 2, 3])), [1, 2, 3]));
