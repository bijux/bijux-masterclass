import assert from 'node:assert/strict'; import test from 'node:test'; import { CommandRegistry } from '../src/index.js';
test('baseline registry rejects duplicate names',()=>{ const r=new CommandRegistry(); r.register('x',()=>1); assert.throws(()=>r.register('x',()=>2)); assert.deepEqual(r.names(),['x']); });
