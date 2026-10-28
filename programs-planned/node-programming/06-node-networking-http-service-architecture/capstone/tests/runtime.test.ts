import test from 'node:test';
import assert from 'node:assert/strict';
import { defaultLimits } from '../src/config.js';
import { discoverService } from '../src/discovery.js';
import { startServiceWire } from '../src/runtime.js';

test('starts and closes a multi-transport runtime idempotently', async () => {
  const runtime = await startServiceWire({
    limits: { ...defaultLimits, shutdownGraceMs: 100 },
    http: { host: '127.0.0.1', port: 0 },
    http2: { host: '127.0.0.1', port: 0 },
    discovery: { host: '127.0.0.1', port: 0 },
  });
  try {
    const endpoint = runtime.endpoints.discovery;
    assert.ok(endpoint);
    const found = await discoverService({ host: endpoint.host, port: endpoint.port, budgetMs: 500 });
    assert.equal(found.url, new URL(runtime.endpoints.http ?? '').toString());
  } finally {
    const [a, b] = await Promise.all([runtime.close(), runtime.close()]);
    assert.deepEqual(a, b);
    assert.equal(a.cleanupErrors.length, 0);
  }
});
