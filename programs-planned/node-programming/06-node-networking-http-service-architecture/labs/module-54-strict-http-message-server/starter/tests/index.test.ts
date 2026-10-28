import assert from 'node:assert/strict';
import test from 'node:test';
import { jsonBytes } from '../src/index.js';

test('serializes finite JSON bytes', () => {
  assert.equal(jsonBytes({ ok: true }).toString(), '{"ok":true}');
});
