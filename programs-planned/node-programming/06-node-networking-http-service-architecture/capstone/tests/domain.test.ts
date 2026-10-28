import test from 'node:test';
import assert from 'node:assert/strict';
import { fingerprintCommand, parseIdempotencyKey, parseJobId, validateSubmitCommand } from '../src/domain.js';

test('validates commands and stable identifiers', () => {
  assert.equal(validateSubmitCommand({ operation: 'uppercase', payload: 'x' }).operation, 'uppercase');
  assert.equal(parseJobId('job-000001'), 'job-000001');
  assert.equal(parseIdempotencyKey('request-0001'), 'request-0001');
  assert.equal(fingerprintCommand({ operation: 'uppercase', payload: 'x' }), fingerprintCommand({ operation: 'uppercase', payload: 'x' }));
  assert.throws(() => validateSubmitCommand({ operation: 'uppercase', payload: 'x', extra: true }), /exactly/);
});
