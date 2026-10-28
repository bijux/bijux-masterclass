import assert from 'node:assert/strict';
import test from 'node:test';
import { Deadline, parseEndpoint, type Clock } from '../src/index.js';

test('parses a logical HTTPS endpoint without resolving it', () => {
  assert.deepEqual(parseEndpoint('https://localhost/v1/jobs'), {
    scheme: 'https:',
    hostname: 'localhost',
    port: 443,
  });
});

test('deadline reports a shared remaining budget', () => {
  let now = 10;
  const clock: Clock = { nowMs: () => now };
  const deadline = new Deadline(100, clock);
  now = 65;
  assert.equal(deadline.remainingMs(), 45);
});
