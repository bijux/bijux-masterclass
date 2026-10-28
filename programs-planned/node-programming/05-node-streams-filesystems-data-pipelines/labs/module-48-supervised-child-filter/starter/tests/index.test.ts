import test from 'node:test';
import assert from 'node:assert/strict';
import { validateCommand } from '../src/index.js';
test('accepts direct argument vector', () => assert.doesNotThrow(() => validateCommand({ program: process.execPath, args: ['-e', 'console.log(1)'] })));
test('rejects NUL', () => assert.throws(() => validateCommand({ program: 'x', args: ['a\0b'] }), /NUL/));
