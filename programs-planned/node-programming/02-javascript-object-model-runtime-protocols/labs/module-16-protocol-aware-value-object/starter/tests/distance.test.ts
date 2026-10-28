import assert from 'node:assert/strict'; import test from 'node:test'; import { Distance } from '../src/index.js';
test('baseline validates and compares distance',()=>{assert.equal(new Distance(10).equals(new Distance(10)),true);assert.throws(()=>new Distance(-1));});
