import test from 'node:test';
import assert from 'node:assert/strict';
import { settleOne } from '../src/index.js';

test('starter observes one fulfillment and one rejection', async () => {
  assert.deepEqual(await settleOne(async () => 3), { status: 'fulfilled', value: 3 });
  const failed = await settleOne(async () => { throw new Error('no'); });
  assert.equal(failed.status, 'rejected');
});
