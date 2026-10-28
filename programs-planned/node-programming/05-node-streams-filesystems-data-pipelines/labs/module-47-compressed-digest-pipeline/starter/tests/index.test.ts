import test from 'node:test';
import assert from 'node:assert/strict';
import { sha256 } from '../src/index.js';
test('hash is deterministic', () => assert.equal(sha256(Buffer.from('a')), sha256(Buffer.from('a'))));
