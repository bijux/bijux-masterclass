import assert from 'node:assert/strict'; import test from 'node:test'; import { ownPropertyAudit } from '../src/index.js';
test('baseline audits descriptors without getter reads',()=>{let reads=0;const o={};Object.defineProperty(o,'x',{get(){reads+=1;return 1;},enumerable:true});assert.equal(ownPropertyAudit(o)[0]?.kind,'accessor');assert.equal(reads,0);});
