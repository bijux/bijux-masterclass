import test from 'node:test';
import assert from 'node:assert/strict';
import { stagePath } from '../src/index.js';
test('stage is beside destination', () => assert.equal(stagePath('/tmp/out.txt', 'x'), '/tmp/.out.txt.x.tmp'));
