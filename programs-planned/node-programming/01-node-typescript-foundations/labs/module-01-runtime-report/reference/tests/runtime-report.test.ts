import test from 'node:test';
import assert from 'node:assert/strict';
import { buildRuntimeReport, parseNodeVersion, renderRuntimeReport } from '../src/index.js';

test('parses an exact version', () => {
  assert.deepEqual(parseNodeVersion('v24.19.0'), { major: 24, minor: 19, patch: 0 });
});

for (const invalid of ['24.19.0', 'v24.19', 'v24.19.0x', ' v24.19.0', 'v-1.0.0', 'v1.2.9007199254740992']) {
  test(`rejects ${JSON.stringify(invalid)}`, () => {
    assert.throws(() => parseNodeVersion(invalid), /invalid|safe integer/);
  });
}

test('renders deterministic fields', () => {
  const report = buildRuntimeReport({
    version: 'v24.19.0', platform: 'linux', architecture: 'x64', executable: '/opt/node', moduleMode: 'esm',
  });
  assert.equal(renderRuntimeReport(report),
    'version\tv24.19.0\nmajor\t24\nsupported\ttrue\nplatform\tlinux\narchitecture\tx64\nexecutable\t/opt/node\nmodule-mode\tesm\n');
});
