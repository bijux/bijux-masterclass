import assert from 'node:assert/strict';
import http2 from 'node:http2';
import test from 'node:test';
import { once } from 'node:events';
import { h2Request, startHttp2Service } from '../src/index.js';

test('multiplexes independent streams without completion-order assumptions', async () => {
  const server = await startHttp2Service({ maxBodyBytes: 32, maxSessions: 2, maxStreams: 8 });
  const session = http2.connect(server.authority);
  await once(session, 'connect');
  const [slow, health, echo] = await Promise.all([
    h2Request(session, { method: 'GET', path: '/slow?ms=20' }),
    h2Request(session, { method: 'GET', path: '/health' }),
    h2Request(session, { method: 'POST', path: '/echo', body: Buffer.from('abc') }),
  ]);
  assert.equal(slow.body.toString(), '20');
  assert.equal(JSON.parse(health.body.toString()).ok, true);
  assert.equal(echo.body.toString(), 'abc');
  session.close();
  await once(session, 'close');
  await server.close();
});

test('bounds each stream body', async () => {
  const server = await startHttp2Service({ maxBodyBytes: 3, maxSessions: 2, maxStreams: 8 });
  const session = http2.connect(server.authority);
  await once(session, 'connect');
  const response = await h2Request(session, { method: 'POST', path: '/echo', body: Buffer.from('abcd') });
  assert.equal(response.status, 413);
  session.close();
  await once(session, 'close');
  await server.close();
});

test('one reset stream does not invalidate the session', async () => {
  const server = await startHttp2Service({ maxBodyBytes: 32, maxSessions: 2, maxStreams: 8 });
  const session = http2.connect(server.authority);
  await once(session, 'connect');
  await assert.rejects(h2Request(session, { method: 'GET', path: '/slow?ms=50', reset: true }));
  const health = await h2Request(session, { method: 'GET', path: '/health' });
  assert.equal(health.status, 200);
  session.close();
  await once(session, 'close');
  await server.close();
});

test('closes sessions and streams under bounded shutdown', async () => {
  const server = await startHttp2Service({ maxBodyBytes: 32, maxSessions: 2, maxStreams: 8 });
  const session = http2.connect(server.authority);
  await once(session, 'connect');
  assert.equal(server.sessions(), 1);
  await server.close(0);
  assert.equal(server.sessions(), 0);
  session.destroy();
});
