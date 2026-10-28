import assert from 'node:assert/strict';
import test from 'node:test';
import { AuditService } from '../src/index.js';

test('health and readiness are separate state', () => {
  const service = new AuditService();
  assert.equal(service.health().readiness, 'not-ready');
  service.markReady();
  assert.equal(service.health().readiness, 'ready');
});
