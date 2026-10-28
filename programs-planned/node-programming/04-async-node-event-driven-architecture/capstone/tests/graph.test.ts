import test from 'node:test';
import assert from 'node:assert/strict';
import { parseManifest } from '../src/manifest.js';
import { TaskGraph } from '../src/graph.js';

test('graph emits deterministic topological order', () => {
  const graph = TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [
    { id: 'a', kind: 'echo', text: 'a' }, { id: 'b', kind: 'echo', text: 'b' },
    { id: 'c', kind: 'echo', text: 'c', dependsOn: ['a', 'b'] },
  ] }));
  assert.deepEqual(graph.topologicalOrder, ['a', 'b', 'c']);
});

test('unknown dependencies and cycles fail before execution', () => {
  assert.throws(() => TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [{ id: 'a', kind: 'echo', text: 'a', dependsOn: ['x'] }] })), /unknown/);
  assert.throws(() => TaskGraph.validate(parseManifest({ version: 'TASK_HARBOR_V1', tasks: [
    { id: 'a', kind: 'echo', text: 'a', dependsOn: ['b'] }, { id: 'b', kind: 'echo', text: 'b', dependsOn: ['a'] },
  ] })), /cycle/);
});
