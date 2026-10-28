import assert from 'node:assert/strict'; import test from 'node:test'; import { normalizeName, validateBalance } from '../src/index.js';
test('baseline validates primitive invariants',()=>{assert.equal(normalizeName(' a '),'a');assert.equal(validateBalance(0),0);assert.throws(()=>validateBalance(-1));});
