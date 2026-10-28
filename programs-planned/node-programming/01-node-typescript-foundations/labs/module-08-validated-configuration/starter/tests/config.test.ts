import test from 'node:test';
import assert from 'node:assert/strict';
import { issue } from '../src/index.js';

test('constructs path-aware issue', () => assert.deepEqual(issue('mode', 'invalid'), { path: 'mode', message: 'invalid' }));
