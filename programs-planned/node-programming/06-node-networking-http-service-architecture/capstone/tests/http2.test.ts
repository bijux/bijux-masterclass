import test from 'node:test';
import assert from 'node:assert/strict';
import http2 from 'node:http2';
import { defaultLimits } from '../src/config.js';
import { startHttp2Server } from '../src/http2.js';
import { ServiceWireApplication } from '../src/service.js';

function h2Request(session: http2.ClientHttp2Session, path: string): Promise<{status:number; body:string}> {
  return new Promise((resolve, reject) => {
    const stream = session.request({ ':method': 'GET', ':path': path });
    let status = 0; const chunks: Buffer[] = [];
    stream.on('response', (headers) => { status = Number(headers[':status'] ?? 0); });
    stream.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
    stream.on('end', () => resolve({ status, body: Buffer.concat(chunks).toString('utf8') }));
    stream.on('error', reject);
    stream.end();
  });
}

test('serves concurrent HTTP/2 streams over one session', async () => {
  const app = new ServiceWireApplication(defaultLimits);
  const server = await startHttp2Server({ application: app, limits: defaultLimits, host: '127.0.0.1', port: 0 });
  const session = http2.connect(server.authority);
  try {
    const [health, stats] = await Promise.all([h2Request(session, '/v1/health'), h2Request(session, '/v1/stats')]);
    assert.equal(health.status, 200);
    assert.equal(stats.status, 200);
  } finally {
    session.close();
    await new Promise<void>((resolve) => session.once('close', () => resolve()));
    await server.close();
    await app.close();
  }
});
