import assert from 'node:assert/strict'; import test from 'node:test'; import { validateNodes } from '../src/index.js';
test('baseline validates unique nodes',()=>{assert.equal(validateNodes([{id:'a',children:[]}]).size,1);assert.throws(()=>validateNodes([{id:'a',children:[]},{id:'a',children:[]}]))});
