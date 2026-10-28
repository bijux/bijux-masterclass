import assert from 'node:assert/strict';
import test from 'node:test';

import { decodeEnvelope, encodeEnvelope, HEADER_BYTES } from '../src/index.js';

test('round trips the canonical big-endian envelope', () => {
  const encoded = encodeEnvelope(0x1234, Buffer.from('hello'), 16);
  assert.equal(encoded.readUInt16BE(1), 0x1234);
  assert.equal(encoded.readUInt32BE(3), 5);
  assert.deepEqual(
    decodeEnvelope(encoded, { maxPayloadBytes: 16 }),
    { version: 1, kind: 0x1234, payload: Buffer.from('hello') },
  );
});

test('encoding respects the visible Uint8Array window', () => {
  const backing = Uint8Array.from([99, 1, 2, 3, 88]);
  const encoded = encodeEnvelope(7, backing.subarray(1, 4), 3);
  assert.deepEqual(
    decodeEnvelope(encoded, { maxPayloadBytes: 3 }).payload,
    Buffer.from([1, 2, 3]),
  );
});

test('owned payload survives source mutation', () => {
  const encoded = encodeEnvelope(7, Buffer.from([1, 2]), 8);
  const decoded = decodeEnvelope(encoded, { maxPayloadBytes: 8 });
  encoded[HEADER_BYTES] = 9;
  assert.deepEqual([...decoded.payload], [1, 2]);
});

test('view mode exposes deliberate aliasing', () => {
  const encoded = encodeEnvelope(7, Buffer.from([1, 2]), 8);
  const decoded = decodeEnvelope(encoded, {
    maxPayloadBytes: 8,
    copyPayload: false,
  });
  encoded[HEADER_BYTES] = 9;
  assert.equal(decoded.payload[0], 9);
});

test('rejects invalid kind and bound arguments', () => {
  assert.throws(() => encodeEnvelope(-1, Buffer.alloc(0), 0), /unsigned/);
  assert.throws(() => encodeEnvelope(0x1_0000, Buffer.alloc(0), 0), /unsigned/);
  assert.throws(() => encodeEnvelope(1, Buffer.alloc(0), -1), /non-negative/);
});

test('rejects truncation, unsupported versions, trailing bytes, and limits', () => {
  assert.throws(
    () => decodeEnvelope(Buffer.alloc(2), { maxPayloadBytes: 8 }),
    /truncated/,
  );

  const valid = encodeEnvelope(1, Buffer.from([1]), 8);
  const unsupported = Buffer.from(valid);
  unsupported[0] = 2;
  assert.throws(
    () => decodeEnvelope(unsupported, { maxPayloadBytes: 8 }),
    /unsupported version 2/,
  );
  assert.throws(
    () => decodeEnvelope(Buffer.concat([valid, Buffer.from([0])]), {
      maxPayloadBytes: 8,
    }),
    /length/,
  );
  assert.throws(
    () => decodeEnvelope(valid, { maxPayloadBytes: 0 }),
    /limit/,
  );
});
