import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { defaultLimits } from '../src/config.js';
import { startHttp1Server } from '../src/http1.js';
import { ServiceWireApplication } from '../src/service.js';

function request(url: string, method: string, body?: string, headers: Record<string, string> = {}): Promise<{status:number; headers:http.IncomingHttpHeaders; body:string}> {
  return new Promise((resolve, reject) => {
    const req = http.request(url, { method, headers }, (res) => {
      const chunks: Buffer[] = [];
      res.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
      res.on('end', () => resolve({ status: res.statusCode ?? 0, headers: res.headers, body: Buffer.concat(chunks).toString('utf8') }));
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

test('serves strict HTTP routes and idempotent submission', async () => {
  const app = new ServiceWireApplication(defaultLimits);
  const server = await startHttp1Server({ application: app, limits: defaultLimits, host: '127.0.0.1', port: 0 });
  try {
    const payload = JSON.stringify({ operation: 'uppercase', payload: 'hello' });
    const first = await request(`${server.url}/v1/jobs`, 'POST', payload, {
      'content-type': 'application/json',
      'content-length': String(Buffer.byteLength(payload)),
      'idempotency-key': 'request-0001',
    });
    assert.equal(first.status, 202);
    assert.equal(typeof first.headers.etag, 'string');
    const repeated = await request(`${server.url}/v1/jobs`, 'POST', payload, {
      'content-type': 'application/json',
      'content-length': String(Buffer.byteLength(payload)),
      'idempotency-key': 'request-0001',
    });
    assert.equal(JSON.parse(repeated.body).replay, true);
    const method = await request(`${server.url}/v1/health`, 'POST');
    assert.equal(method.status, 405);
    assert.equal(method.headers.allow, 'GET, HEAD');
  } finally {
    await server.close();
    await app.close();
  }
});
