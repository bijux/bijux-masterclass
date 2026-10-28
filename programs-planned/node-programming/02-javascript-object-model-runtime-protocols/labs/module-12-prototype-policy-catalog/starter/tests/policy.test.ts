import assert from 'node:assert/strict'; import test from 'node:test';
import { createDefaultPolicy } from '../src/index.js';
test('baseline freezes validated defaults', () => { const p=createDefaultPolicy({maxItems:10,retentionDays:30}); assert.equal(Object.isFrozen(p), true); assert.throws(()=>createDefaultPolicy({maxItems:0,retentionDays:1})); });
