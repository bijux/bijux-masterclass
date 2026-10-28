import test from 'node:test';
import assert from 'node:assert/strict';
import { encodeFlowEvent, parseFlowEvent } from '../src/domain.js';
const limits = { maxIdBytes: 32, maxKindBytes: 32 };
test('validates exact event and canonical order', () => { const event = parseFlowEvent({ kind: 'sale', value: 2, id: 'e1', timestamp: '2026-08-09T10:00:00.000Z' }, limits); assert.equal(encodeFlowEvent(event).toString(), '{"id":"e1","timestamp":"2026-08-09T10:00:00.000Z","kind":"sale","value":2}\n'); });
test('rejects unknown keys and noncanonical timestamp', () => { assert.throws(() => parseFlowEvent({ id: 'e1', timestamp: '2026-08-09', kind: 'x', value: 1 }, limits)); assert.throws(() => parseFlowEvent({ id: 'e1', timestamp: '2026-08-09T10:00:00.000Z', kind: 'x', value: 1, extra: true }, limits)); });
