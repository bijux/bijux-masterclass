import test from 'node:test';
import assert from 'node:assert/strict';
import { ByteCounter } from '../src/index.js';
test('counts bytes passing through', () => { const counter = new ByteCounter(); counter.write(Buffer.from('ab')); counter.end(Buffer.from('c')); assert.equal(counter.bytes, 3); });
