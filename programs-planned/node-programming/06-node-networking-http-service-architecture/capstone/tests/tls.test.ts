import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { ServiceWireClient } from '../src/client.js';
import { defaultLimits } from '../src/config.js';
import { startHttp1Server } from '../src/http1.js';
import { ServiceWireApplication } from '../src/service.js';

const fixtures = new URL('../../fixtures/tls/', import.meta.url);

test('verifies local TLS identity with an explicit course CA', async () => {
  const [key, cert, ca] = await Promise.all([
    readFile(new URL('server-key.pem', fixtures)),
    readFile(new URL('server-cert.pem', fixtures)),
    readFile(new URL('ca-cert.pem', fixtures)),
  ]);
  const app = new ServiceWireApplication(defaultLimits);
  const server = await startHttp1Server({ application: app, limits: defaultLimits, host: '127.0.0.1', port: 0, tls: { key, cert } });
  const client = new ServiceWireClient({ baseUrl: new URL(server.url), maxSockets: 1, maxResponseBytes: 100_000, maxAttempts: 1, ca, servername: 'localhost' });
  try { assert.equal((await client.health()).health, 'healthy'); }
  finally { client.close(); await server.close(); await app.close(); }
});
