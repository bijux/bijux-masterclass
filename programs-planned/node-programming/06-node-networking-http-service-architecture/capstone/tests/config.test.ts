import test from 'node:test';
import assert from 'node:assert/strict';
import { defaultLimits, validateLimits, validateListenConfig } from '../src/config.js';

test('validates capacity relationships and ephemeral ports', () => {
  assert.equal(validateLimits(defaultLimits).maxJobs, 256);
  assert.deepEqual(validateListenConfig({ host: '127.0.0.1', port: 0 }), { host: '127.0.0.1', port: 0 });
  assert.throws(() => validateLimits({ ...defaultLimits, maxActiveJobs: 300 }), /maxActiveJobs/);
});
