import assert from 'node:assert/strict';
import test from 'node:test';
import { HttpClient } from '../src/index.js';

test('closed clients reject new work', async () => {
  const client = new HttpClient();
  client.close();
  await assert.rejects(client.get(new URL('http://127.0.0.1:1')), /closed/);
});
