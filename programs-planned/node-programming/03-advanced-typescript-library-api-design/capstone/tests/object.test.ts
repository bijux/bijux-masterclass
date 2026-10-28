import assert from 'node:assert/strict';
import test from 'node:test';
import { literal, number, object, optional, string } from '../src/index.js';

test('object schema distinguishes missing optional fields from present undefined', () => {
  const User = object({ format: literal('USER_V1'), name: string(), age: optional(number()) });
  const absent = User.parse({ format: 'USER_V1', name: 'Ada' });
  assert.deepEqual({ ...absent }, { format: 'USER_V1', name: 'Ada' });
  const present = User.safeParse({ format: 'USER_V1', name: 'Ada', age: undefined });
  assert.equal(present.ok, false);
});

test('object schema ignores inherited properties and rejects unknown own keys', () => {
  const Base = object({ name: string() });
  const inherited = Object.create({ name: 'inherited' }) as Record<string, unknown>;
  assert.equal(Base.safeParse(inherited).ok, false);
  assert.equal(Base.safeParse({ name: 'Ada', role: 'admin' }).ok, false);
  assert.deepEqual({ ...object({ name: string() }, { unknownKeys: 'strip' }).parse({ name: 'Ada', role: 'admin' }) }, { name: 'Ada' });
});
