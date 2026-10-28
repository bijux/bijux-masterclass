import assert from 'node:assert/strict';
import test from 'node:test';
import {
  ConnectionExhaustedError,
  Deadline,
  listenEphemeral,
  parseEndpoint,
  planConnection,
  type AddressCandidate,
  type Clock,
  type ConnectionHandle,
} from '../src/index.js';

test('parses IPv6 and default ports without resolving names', () => {
  assert.deepEqual(parseEndpoint('http://[::1]/v1'), {
    scheme: 'http:',
    hostname: '[::1]',
    port: 80,
  });
});

test('uses one deadline across candidate failures', async () => {
  let now = 0;
  const clock: Clock = { nowMs: () => now };
  const candidates: readonly AddressCandidate[] = [
    { address: '::1', family: 6 },
    { address: '127.0.0.1', family: 4 },
  ];
  const seen: number[] = [];
  const handle: ConnectionHandle = {
    localAddress: '127.0.0.1:50000',
    peerAddress: '127.0.0.1:80',
    close() {},
  };

  const result = await planConnection(
    parseEndpoint('http://service.test'),
    async () => candidates,
    async (_endpoint, candidate, remaining) => {
      seen.push(Math.round(remaining));
      if (candidate.family === 6) {
        now += 70;
        throw Object.assign(new Error('refused'), { code: 'ECONNREFUSED' });
      }
      now += 10;
      return handle;
    },
    { budgetMs: 100, clock },
  );

  assert.equal(result.candidate.family, 4);
  assert.deepEqual(seen, [100, 30]);
  assert.equal(result.attempts.length, 2);
});

test('does not begin another candidate after expiry', async () => {
  let now = 0;
  const clock: Clock = { nowMs: () => now };
  let calls = 0;
  await assert.rejects(
    planConnection(
      parseEndpoint('http://service.test'),
      async () => [
        { address: '192.0.2.1', family: 4 as const },
        { address: '192.0.2.2', family: 4 as const },
      ],
      async () => {
        calls += 1;
        now += 50;
        throw new Error('failed');
      },
      { budgetMs: 40, clock },
    ),
    ConnectionExhaustedError,
  );
  assert.equal(calls, 1);
});

test('binds the actual server directly to an ephemeral port', async () => {
  const listener = await listenEphemeral();
  assert.ok(listener.port > 0);
  assert.equal(listener.server.listening, true);
  await listener.close();
  assert.equal(listener.server.listening, false);
});

test('deadline validates its budget', () => {
  assert.throws(() => new Deadline(0), /positive/);
});
