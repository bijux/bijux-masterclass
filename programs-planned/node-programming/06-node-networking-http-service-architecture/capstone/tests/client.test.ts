import test from 'node:test';
import assert from 'node:assert/strict';
import { ServiceWireClient } from '../src/client.js';
import { defaultLimits } from '../src/config.js';
import { startHttp1Server } from '../src/http1.js';
import { ServiceWireApplication } from '../src/service.js';

test('supported client owns pooling, response bounds, and job polling', async () => {
  const app = new ServiceWireApplication(defaultLimits);
  const server = await startHttp1Server({ application: app, limits: defaultLimits, host: '127.0.0.1', port: 0 });
  const client = new ServiceWireClient({ baseUrl: new URL(server.url), maxSockets: 2, maxResponseBytes: 200_000, maxAttempts: 2 });
  try {
    const submitted = await client.submit({ operation: 'word-count', payload: 'one two three' }, 'request-0003');
    const terminal = await client.waitForTerminal(submitted.job.id, 1_000);
    assert.equal(terminal.result, '3');
    assert.equal((await client.health()).readiness, 'ready');
  } finally {
    client.close();
    await server.close();
    await app.close();
  }
});
