import assert from 'node:assert/strict';
import test from 'node:test';
import { matchRoute } from '../src/index.js';

test('matches a typed job route', () => {
  assert.deepEqual(matchRoute('GET', new URL('http://x/jobs/job-1')), {
    kind: 'job',
    id: 'job-1',
  });
});
