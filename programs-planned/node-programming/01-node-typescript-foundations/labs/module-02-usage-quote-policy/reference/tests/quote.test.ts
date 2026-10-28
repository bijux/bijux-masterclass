import test from 'node:test';
import assert from 'node:assert/strict';
import { formatCents, parseUnits, quoteUsage } from '../src/index.js';

test('quotes starter overage', () => {
  assert.deepEqual(quoteUsage('125', 'starter'), {
    plan: 'starter', units: 125, includedUnits: 100, billableUnits: 25, totalCents: 125,
  });
});

test('preserves valid zero-cost values', () => {
  assert.equal(quoteUsage('0', 'starter').totalCents, 0);
  assert.equal(quoteUsage('900000', 'enterprise').totalCents, 0);
});

for (const raw of ['', ' ', '-1', '1.5', '1e3', '12units', '01']) {
  test(`rejects malformed units ${JSON.stringify(raw)}`, () => assert.throws(() => parseUnits(raw)));
}

test('rejects unsupported plan independently', () => {
  assert.throws(() => quoteUsage('10', 'unknown'), /unsupported plan/);
});

test('renders integer cents exactly', () => assert.equal(formatCents(125), '$1.25'));
