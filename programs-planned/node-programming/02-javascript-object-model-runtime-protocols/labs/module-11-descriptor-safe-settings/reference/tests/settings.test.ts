import assert from 'node:assert/strict';
import test from 'node:test';
import { createSettings, describeOwnProperties, settingsSource, snapshotSettings } from '../src/index.js';

test('separates data, accessor, and symbol metadata surfaces', () => {
  const settings = createSettings({ theme: 'dark', retries: 2 }, 'defaults.json');
  assert.deepEqual(Object.keys(settings), ['theme', 'retries']);
  assert.equal(settings.summary, 'retries, theme');
  assert.equal(settingsSource(settings), 'defaults.json');
  assert.deepEqual({ ...settings }, { theme: 'dark', retries: 2 });
  assert.deepEqual({ ...snapshotSettings(settings) }, { theme: 'dark', retries: 2 });
  const reports = describeOwnProperties(settings);
  assert.equal(reports.some((report) => report.key === 'summary' && report.kind === 'accessor'), true);
  assert.equal(reports.some((report) => report.key === 'Symbol(settings.source)'), true);
});

test('inspection and snapshot rejection do not invoke accessors', () => {
  let reads = 0;
  const value = {};
  Object.defineProperty(value, 'danger', { enumerable: true, configurable: true, get() { reads += 1; throw new Error('ran'); } });
  assert.equal(describeOwnProperties(value)[0]?.kind, 'accessor');
  assert.equal(reads, 0);
  assert.throws(() => snapshotSettings(value), /enumerable accessor/);
  assert.equal(reads, 0);
});

test('metadata is permanent', () => {
  const settings = createSettings({}, 'built-in');
  const symbol = Reflect.ownKeys(settings).find((key) => typeof key === 'symbol');
  assert.notEqual(symbol, undefined);
  assert.equal(Reflect.deleteProperty(settings, symbol!), false);
  assert.equal(Reflect.set(settings, symbol!, 'other'), false);
  assert.equal(settingsSource(settings), 'built-in');
});
