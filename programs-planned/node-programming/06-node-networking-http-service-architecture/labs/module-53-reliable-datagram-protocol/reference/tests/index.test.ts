import assert from 'node:assert/strict';
import test from 'node:test';
import {
  ReplayCache, createNonce, decodeResponse, encodeResponse, requestWithRetry,
} from '../src/index.js';

test('creates a 128-bit hexadecimal nonce', () => {
  assert.match(createNonce(), /^[0-9a-f]{32}$/);
});

test('ignores malformed, wrong-peer, stale, and duplicate responses', async () => {
  const nonce = '0123456789abcdef0123456789abcdef';
  const good = encodeResponse({ nonce, url: 'http://127.0.0.1:9000', version: '1' });
  const stale = encodeResponse({
    nonce: 'ffffffffffffffffffffffffffffffff',
    url: 'http://127.0.0.1:9000',
    version: '1',
  });
  const result = await requestWithRetry(
    async (_request, attempt) => attempt === 1 ? [] : [
      { bytes: Buffer.from('garbage'), peer: '127.0.0.1:9' },
      { bytes: stale, peer: 'expected' },
      { bytes: good, peer: 'wrong' },
      { bytes: good, peer: 'expected' },
      { bytes: good, peer: 'expected' },
    ],
    {
      nonce,
      expectedPeer: 'expected',
      budgetMs: 100,
      delaysMs: [1],
      sleep: async () => {},
    },
  );
  assert.equal(result.attempts, 2);
  assert.equal(decodeResponse(good).nonce, nonce);
});

test('replay cache remains bounded and expires entries', () => {
  const cache = new ReplayCache(2, 10);
  cache.set('a', Buffer.from('a'), 0);
  cache.set('b', Buffer.from('b'), 0);
  cache.set('c', Buffer.from('c'), 1);
  assert.equal(cache.get('a', 1), undefined);
  assert.equal(cache.size(1), 2);
  assert.equal(cache.size(11), 0);
});

test('uses one deadline rather than one timeout per retry', async () => {
  let now = 0;
  let attempts = 0;
  await assert.rejects(requestWithRetry(
    async () => { attempts += 1; now += 8; return []; },
    {
      nonce: '0123456789abcdef0123456789abcdef',
      expectedPeer: 'expected',
      budgetMs: 10,
      delaysMs: [5, 5],
      now: () => now,
      sleep: async (ms) => { now += ms; },
    },
  ));
  assert.equal(attempts, 1);
});
