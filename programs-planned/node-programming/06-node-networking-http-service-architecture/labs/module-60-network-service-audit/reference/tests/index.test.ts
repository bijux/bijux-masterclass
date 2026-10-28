import assert from 'node:assert/strict';
import test from 'node:test';
import { AuditService, type OwnedResource } from '../src/index.js';

test('rolls startup back in reverse order', async () => {
  const closed: string[] = [];
  await assert.rejects(AuditService.start({
    maxJobs: 4,
    maxActive: 1,
    resourceNames: ['http', 'h2', 'udp'],
    createResource: async (name): Promise<OwnedResource> => {
      if (name === 'udp') throw new Error('bind failed');
      return { name, close: async () => { closed.push(name); } };
    },
  }), /bind failed/);
  assert.deepEqual(closed, ['h2', 'http']);
});

test('separates readiness from liveness and rejects during quiesce', async () => {
  const service = await AuditService.start({
    maxJobs: 2,
    maxActive: 1,
    resourceNames: [],
    createResource: async (name) => ({ name, close: async () => {} }),
  });
  assert.equal(service.health().readiness, 'ready');
  const closing = service.close(0);
  assert.throws(() => service.submit(1), /NOT_READY/);
  const report = await closing;
  assert.equal(report.acceptedJobs, 0);
});

test('uses one grace period then cancels remaining work', async () => {
  const service = await AuditService.start({
    maxJobs: 4,
    maxActive: 1,
    resourceNames: ['http'],
    createResource: async (name) => ({ name, close: async () => {} }),
  });
  service.submit(100);
  service.submit(100);
  const report = await service.close(0);
  assert.equal(report.acceptedJobs, 2);
  assert.equal(report.cancelledJobs, 2);
  assert.equal(report.closedResources, 1);
});

test('reconciles subscribers and makes close idempotent', async () => {
  const service = await AuditService.start({
    maxJobs: 2,
    maxActive: 1,
    resourceNames: [],
    createResource: async (name) => ({ name, close: async () => {} }),
  });
  const subscription = service.subscribe();
  subscription.dispose();
  const first = service.close(10);
  const second = service.close(10);
  assert.equal(first, second);
  const report = await first;
  assert.equal(report.openedSubscribers, 1);
  assert.equal(report.closedSubscribers, 1);
});
