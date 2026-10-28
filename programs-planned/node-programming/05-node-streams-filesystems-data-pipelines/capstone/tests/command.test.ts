import test from 'node:test';
import assert from 'node:assert/strict';
import { parseCommand } from '../src/command.js';
test('parses filter options independently of position', () => assert.deepEqual(parseCommand(['filter', 'in', 'out', '--gzip-output', '--kind', 'sale', '--replace']), { kind: 'filter', input: 'in', output: 'out', selectedKind: 'sale', gzipInput: false, gzipOutput: true, replace: true }));
test('requires through delimiter', () => assert.throws(() => parseCommand(['through', 'in', 'out', 'node']), /requires --/));
test('validates digest syntax', () => assert.throws(() => parseCommand(['verify', 'x', '--sha256', 'no']), /64/));
