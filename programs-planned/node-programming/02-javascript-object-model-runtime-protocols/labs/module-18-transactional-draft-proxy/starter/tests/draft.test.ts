import assert from 'node:assert/strict'; import test from 'node:test'; import { copyRecord, validateKey } from '../src/index.js';
test('baseline creates an independent null-prototype record',()=>{const s={a:1};const c=copyRecord(s);c.a=2;assert.equal(s.a,1);assert.equal(Object.getPrototypeOf(c),null);assert.throws(()=>validateKey('__proto__'));});
