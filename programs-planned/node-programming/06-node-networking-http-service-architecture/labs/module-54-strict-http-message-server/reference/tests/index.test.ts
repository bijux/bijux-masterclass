import assert from 'node:assert/strict';
import http from 'node:http';
import test from 'node:test';
import { startStrictServer } from '../src/index.js';

async function request(
  url: string,
  options: { readonly method: string; readonly headers?: Record<string, string>; readonly body?: Buffer },
): Promise<{ readonly status: number; readonly headers: http.IncomingHttpHeaders; readonly body: Buffer }> {
  return await new Promise((resolve, reject) => {
    const req = http.request(url, { method: options.method, headers: options.headers }, (res) => {
      const chunks: Buffer[] = [];
      res.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
      res.on('end', () => resolve({
        status: res.statusCode ?? 0,
        headers: res.headers,
        body: Buffer.concat(chunks),
      }));
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

test('GET and HEAD share metadata but HEAD sends no body', async () => {
  const server = await startStrictServer({ maxBodyBytes: 32, maxConnections: 4 });
  const get = await request(`${server.url}/health`, { method: 'GET' });
  const head = await request(`${server.url}/health`, { method: 'HEAD' });
  assert.equal(get.status, 200);
  assert.equal(head.status, 200);
  assert.equal(head.body.byteLength, 0);
  assert.equal(head.headers['content-length'], get.headers['content-length']);
  await server.close();
});

test('enforces observed body limit and does not invoke domain work', async () => {
  const server = await startStrictServer({ maxBodyBytes: 8, maxConnections: 4 });
  const response = await request(`${server.url}/echo`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: Buffer.from('{"value":"too large"}'),
  });
  assert.equal(response.status, 413);
  assert.equal(server.calls(), 0);
  await server.close();
});

test('separates media, syntax, and shape failures', async () => {
  const server = await startStrictServer({ maxBodyBytes: 64, maxConnections: 4 });
  assert.equal((await request(`${server.url}/echo`, { method: 'POST', body: Buffer.from('{}') })).status, 415);
  assert.equal((await request(`${server.url}/echo`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: Buffer.from('{'),
  })).status, 400);
  assert.equal((await request(`${server.url}/echo`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: Buffer.from('[]'),
  })).status, 422);
  await server.close();
});

test('returns 405 with Allow and bounds request IDs', async () => {
  const server = await startStrictServer({ maxBodyBytes: 64, maxConnections: 4 });
  const response = await request(`${server.url}/health`, {
    method: 'POST',
    headers: { 'x-request-id': 'known-id' },
  });
  assert.equal(response.status, 405);
  assert.equal(response.headers.allow, 'GET, HEAD');
  assert.equal(response.headers['x-request-id'], 'known-id');
  await server.close();
});

test('quiescing rejects new application work', async () => {
  const server = await startStrictServer({ maxBodyBytes: 64, maxConnections: 4 });
  server.quiesce();
  const response = await request(`${server.url}/echo`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: Buffer.from('{}'),
  });
  assert.equal(response.status, 503);
  await server.close();
  assert.equal(server.activeRequests(), 0);
});
