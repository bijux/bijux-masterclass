import test from 'node:test';
import assert from 'node:assert/strict';
import { defaultLimits } from '../src/config.js';
import { parseIdempotencyKey } from '../src/domain.js';
import { ServiceWireApplication } from '../src/service.js';

test('deduplicates submissions and reaches a terminal state', async () => {
  const app = new ServiceWireApplication({ ...defaultLimits, maxActiveJobs: 1 });
  const key = parseIdempotencyKey('request-0001');
  const first = app.submit({ operation: 'uppercase', payload: 'hello' }, key);
  const replay = app.submit({ operation: 'uppercase', payload: 'hello' }, key);
  assert.equal(replay.replay, true);
  assert.equal(replay.job.id, first.job.id);
  assert.equal(await app.waitForIdle(500), true);
  const found = app.getJob(first.job.id as never);
  assert.equal(found?.job.state, 'succeeded');
  assert.equal(found?.job.result, 'HELLO');
  const report = await app.close();
  assert.equal(report.succeededJobs, 1);
});

test('shutdown classifies aborted work as cancelled', async () => {
  const app = new ServiceWireApplication({ ...defaultLimits, maxActiveJobs: 1, shutdownGraceMs: 1 });
  app.submit({ operation: 'sleep', payload: '500' }, parseIdempotencyKey('request-0002'));
  await new Promise((resolve) => setTimeout(resolve, 5));
  const report = await app.close(1);
  assert.equal(report.cancelledJobs, 1);
  assert.equal(report.failedJobs, 0);
});
