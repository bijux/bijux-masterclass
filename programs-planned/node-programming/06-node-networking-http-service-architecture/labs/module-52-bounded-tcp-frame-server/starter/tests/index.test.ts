import assert from 'node:assert/strict';
import test from 'node:test';
import { encodeFrame, FrameDecoder } from '../src/index.js';

test('decodes a complete frame', () => {
  const decoder = new FrameDecoder();
  assert.deepEqual(decoder.push(encodeFrame(Buffer.from('hello'))).map(String), ['hello']);
});
