import assert from 'node:assert/strict';
import http from 'node:http';
import test from 'node:test';
import { DeadlineHttpClient, ClientError } from '../src/index.js';

async function localServer(handler: http.RequestListener): Promise<{ url: URL; close(): Promise<void> }> {
  const server = http.createServer(handler);
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  if (address === null || typeof address === 'string') throw new Error('address');
  return {
    url: new URL(`http://127.0.0.1:${address.port}`),
    close: async () => { await new Promise<void>((resolve) => server.close(() => resolve())); },
  };
}

test('reads a bounded response and closes its agent', async () => {
  const server = await localServer((_req, res) => res.end('ok'));
  const client = new DeadlineHttpClient({ maxSockets: 2, maxResponseBytes: 8, maxAttempts: 2 });
  const result = await client.request({ url: server.url, budgetMs: 500 });
  assert.equal(result.body.toString(), 'ok');
  client.close();
  await server.close();
});

test('rejects oversized success and error bodies', async () => {
  const server = await localServer((_req, res) => { res.statusCode = 500; res.end('0123456789'); });
  const client = new DeadlineHttpClient({ maxSockets: 1, maxResponseBytes: 4, maxAttempts: 1 });
  await assert.rejects(client.request({ url: server.url, budgetMs: 500 }), (error) =>
    error instanceof ClientError && error.code === 'RESPONSE_TOO_LARGE');
  client.close();
  await server.close();
});

test('uses same idempotency key when retrying after ambiguous commit', async () => {
  let calls = 0;
  const keys: string[] = [];
  const server = await localServer((req, res) => {
    calls += 1;
    keys.push(String(req.headers['idempotency-key']));
    if (calls === 1) {
      req.socket.destroy();
      return;
    }
    res.statusCode = 202;
    res.end('accepted');
  });
  const client = new DeadlineHttpClient({ maxSockets: 1, maxResponseBytes: 64, maxAttempts: 2 });
  const result = await client.request({
    url: server.url,
    method: 'POST',
    headers: { 'idempotency-key': 'stable-key' },
    body: Buffer.from('{}'),
    budgetMs: 500,
    retry: true,
  });
  assert.equal(result.status, 202);
  assert.deepEqual(keys, ['stable-key', 'stable-key']);
  client.close();
  await server.close();
});

test('applies one deadline and rejects closed clients', async () => {
  const server = await localServer((_req, res) => { setTimeout(() => res.end('late'), 100); });
  const client = new DeadlineHttpClient({ maxSockets: 1, maxResponseBytes: 64, maxAttempts: 2 });
  await assert.rejects(client.request({ url: server.url, budgetMs: 10, retry: true }), (error) =>
    error instanceof ClientError && error.code === 'DEADLINE');
  client.close();
  await assert.rejects(client.request({ url: server.url, budgetMs: 10 }), /closed/);
  await server.close();
});
