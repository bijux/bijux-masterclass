import assert from 'node:assert/strict';
import test from 'node:test';
import { loadFixtures } from '../src/index.js';

test('loads local teaching credentials without rendering key bytes', async () => {
  const fixtures = await loadFixtures();
  assert.match(fixtures.ca.toString('utf8'), /BEGIN CERTIFICATE/);
  assert.match(fixtures.key.toString('utf8'), /BEGIN PRIVATE KEY/);
});
