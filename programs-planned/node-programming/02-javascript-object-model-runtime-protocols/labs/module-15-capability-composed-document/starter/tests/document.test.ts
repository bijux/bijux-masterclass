import assert from 'node:assert/strict'; import test from 'node:test'; import { normalizeTag } from '../src/index.js';
test('baseline normalizes tags',()=>{assert.equal(normalizeTag(' Rust '),'rust');assert.throws(()=>normalizeTag(' '));});
