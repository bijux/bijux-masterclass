import assert from 'node:assert/strict';
import test from 'node:test';
import { responseHeaders } from '../src/index.js';

test('builds HTTP/2 pseudo response headers', () => {
  assert.equal(responseHeaders(200)[':status'], 200);
});
