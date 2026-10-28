import assert from 'node:assert/strict';
import test from 'node:test';
import { once } from 'node:events';
import { connectTls, loadFixtures, startTlsEchoServer } from '../src/index.js';

test('verifies local CA, logical hostname, and ALPN', async () => {
  const fixtures = await loadFixtures();
  const server = await startTlsEchoServer(fixtures, { maxBytes: 64, alpn: ['http/1.1'] });
  const client = await connectTls({
    host: server.host,
    port: server.port,
    servername: 'localhost',
    ca: fixtures.ca,
    requiredAlpn: 'http/1.1',
    budgetMs: 500,
  });
  assert.equal(client.alpnProtocol, 'http/1.1');
  assert.ok(client.peerFingerprint256);
  client.socket.end();
  await once(client.socket, 'close');
  await server.close();
});

test('wrong hostname remains a failure', async () => {
  const fixtures = await loadFixtures();
  const server = await startTlsEchoServer(fixtures, { maxBytes: 64 });
  await assert.rejects(connectTls({
    host: server.host,
    port: server.port,
    servername: 'wrong.example',
    ca: fixtures.ca,
    budgetMs: 500,
  }));
  await server.close();
});

test('untrusted issuer remains a failure', async () => {
  const fixtures = await loadFixtures();
  const server = await startTlsEchoServer(fixtures, { maxBytes: 64 });
  await assert.rejects(connectTls({
    host: server.host,
    port: server.port,
    servername: 'localhost',
    ca: Buffer.from(''),
    budgetMs: 500,
  }));
  await server.close();
});

test('required ALPN mismatch closes the connection', async () => {
  const fixtures = await loadFixtures();
  const server = await startTlsEchoServer(fixtures, { maxBytes: 64, alpn: ['http/1.1'] });
  try {
    await assert.rejects(connectTls({
      host: server.host,
      port: server.port,
      servername: 'localhost',
      ca: fixtures.ca,
      requiredAlpn: 'h2',
      budgetMs: 500,
    }), /ALPN|application protocol/i);
  } finally {
    await server.close();
  }
  assert.equal(server.activeSockets(), 0);
});
