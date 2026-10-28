import assert from 'node:assert/strict';
import test from 'node:test';
import { access, readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

test('package exports publish three aligned runtime and declaration targets', async () => {
  const packageUrl = new URL('../../package.json', import.meta.url);
  const packageText = await readFile(packageUrl, 'utf8');
  const packageValue = JSON.parse(packageText) as {
    readonly exports?: Readonly<Record<string, { readonly types?: string; readonly import?: string }>>;
    readonly files?: readonly string[];
  };
  assert.deepEqual(Object.keys(packageValue.exports ?? {}).sort(), ['.', './json', './testing']);
  const packageRoot = dirname(fileURLToPath(packageUrl));
  for (const [key, target] of Object.entries(packageValue.exports ?? {})) {
    assert.equal(typeof target.types, 'string', `${key} lacks types target`);
    assert.equal(typeof target.import, 'string', `${key} lacks import target`);
    await access(resolve(packageRoot, target.types!));
    await access(resolve(packageRoot, target.import!));
  }
  assert.deepEqual(packageValue.files, ['dist/src', 'README.md']);
});
