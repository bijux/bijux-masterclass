import assert from 'node:assert/strict';
import test from 'node:test';
import { encodeEvent } from '../src/index.js';

test('encodes a complete SSE event', () => {
  assert.equal(
    encodeEvent(1, { type: 'update', data: { ok: true } }).toString(),
    'id: 1\nevent: update\ndata: {"ok":true}\n\n',
  );
});
