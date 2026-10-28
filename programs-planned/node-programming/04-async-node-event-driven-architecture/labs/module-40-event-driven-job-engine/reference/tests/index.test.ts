import test from 'node:test';
import assert from 'node:assert/strict';
import { runJobEngine } from '../src/index.js';

test('dependency success enables dependent and output remains source ordered', async () => {
  const events: string[] = [];
  const outcomes = await runJobEngine([
    { id: 'a', dependsOn: [], run: async () => 1 },
    { id: 'b', dependsOn: ['a'], run: async () => 2 },
  ], { concurrency: 2, onEvent: event => events.push(`${event.type}:${event.id}`) });
  assert.deepEqual(outcomes.map(value => value.status), ['succeeded', 'succeeded']);
  assert.ok(events.indexOf('succeeded:a') < events.indexOf('started:b'));
});

test('failure blocks dependent while independent work succeeds', async () => {
  const outcomes = await runJobEngine([
    { id: 'bad', dependsOn: [], run: async () => { throw new Error('bad'); } },
    { id: 'blocked', dependsOn: ['bad'], run: async () => 2 },
    { id: 'free', dependsOn: [], run: async () => 3 },
  ], { concurrency: 2 });
  assert.deepEqual(outcomes.map(value => value.status), ['failed', 'blocked', 'succeeded']);
});

test('cycle is rejected before execution', async () => {
  let started = false;
  await assert.rejects(runJobEngine([
    { id: 'a', dependsOn: ['b'], run: async () => { started = true; } },
    { id: 'b', dependsOn: ['a'], run: async () => { started = true; } },
  ], { concurrency: 1 }), /cycle/);
  assert.equal(started, false);
});
