import assert from 'node:assert/strict';
import test from 'node:test';
import { createPlainSettings, validateSettingKey } from '../src/index.js';

test('baseline validates keys and copies primitive data', () => {
  assert.equal(validateSettingKey(' theme '), 'theme');
  assert.deepEqual(createPlainSettings({ theme: 'dark', retries: 2 }), { theme: 'dark', retries: 2 });
  assert.throws(() => validateSettingKey('__proto__'));
});
