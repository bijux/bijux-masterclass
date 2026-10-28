import assert from 'node:assert/strict';
import test from 'node:test';
import { decodeRequest, encodeRequest } from '../src/index.js';

test('round trips a bounded discovery request', () => {
  const request = { nonce: '0123456789abcdef0123456789abcdef' };
  assert.deepEqual(decodeRequest(encodeRequest(request)), request);
});
