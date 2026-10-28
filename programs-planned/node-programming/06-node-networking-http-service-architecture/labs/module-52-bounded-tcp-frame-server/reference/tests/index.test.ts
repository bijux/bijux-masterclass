import assert from 'node:assert/strict';
import net from 'node:net';
import test from 'node:test';
import { once } from 'node:events';
import { encodeFrame, FrameDecoder, FrameProtocolError, startFrameServer } from '../src/index.js';

test('decodes the same frames across every single split position', () => {
  const wire = Buffer.concat([encodeFrame(Buffer.from('abc')), encodeFrame(Buffer.from('xy'))]);
  for (let split = 0; split <= wire.byteLength; split += 1) {
    const decoder = new FrameDecoder(10);
    const frames = [...decoder.push(wire.subarray(0, split)), ...decoder.push(wire.subarray(split))];
    decoder.finish();
    assert.deepEqual(frames.map(String), ['abc', 'xy']);
  }
});

test('rejects length before payload allocation', () => {
  const prefix = Buffer.alloc(4);
  prefix.writeUInt32BE(11);
  assert.throws(() => new FrameDecoder(10).push(prefix), (error) =>
    error instanceof FrameProtocolError && error.code === 'FRAME_TOO_LARGE');
});

test('classifies truncated prefix and payload', () => {
  const prefixDecoder = new FrameDecoder(10);
  prefixDecoder.push(Buffer.from([0, 0]));
  assert.throws(() => prefixDecoder.finish(), /TRUNCATED_PREFIX/);

  const payloadDecoder = new FrameDecoder(10);
  payloadDecoder.push(Buffer.from([0, 0, 0, 3, 97]));
  assert.throws(() => payloadDecoder.finish(), /TRUNCATED_PAYLOAD/);
});

test('serves framed responses after client half-close', async () => {
  const server = await startFrameServer({ maxFrameBytes: 32, maxConnections: 4, idleMs: 1000 });
  const socket = net.createConnection({ host: server.host, port: server.port });
  await once(socket, 'connect');
  const decoder = new FrameDecoder(32);
  const output: Buffer[] = [];
  socket.on('data', (chunk) => output.push(...decoder.push(Buffer.from(chunk))));
  socket.end(encodeFrame(Buffer.from('hello')));
  await once(socket, 'close');
  decoder.finish();
  assert.deepEqual(output.map(String), ['HELLO']);
  await server.close();
  assert.equal(server.activeSockets(), 0);
});

test('tracks and destroys sockets during bounded shutdown', async () => {
  const server = await startFrameServer({ maxFrameBytes: 32, maxConnections: 2, idleMs: 5000 });
  const socket = net.createConnection({ host: server.host, port: server.port });
  await once(socket, 'connect');
  assert.equal(server.activeSockets(), 1);
  await server.close(0);
  assert.equal(server.activeSockets(), 0);
});
