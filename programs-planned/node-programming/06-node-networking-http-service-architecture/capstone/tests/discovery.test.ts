import test from 'node:test';
import assert from 'node:assert/strict';
import { discoverService, startDiscoveryServer } from '../src/discovery.js';

test('correlates local UDP discovery by nonce', async () => {
  const server = await startDiscoveryServer({ host: '127.0.0.1', port: 0, advertisedUrl: 'http://127.0.0.1:9999' });
  try {
    const found = await discoverService({ host: '127.0.0.1', port: server.port, budgetMs: 500 });
    assert.equal(found.url, 'http://127.0.0.1:9999/');
    assert.ok(found.attempts >= 1);
  } finally { await server.close(); }
});
