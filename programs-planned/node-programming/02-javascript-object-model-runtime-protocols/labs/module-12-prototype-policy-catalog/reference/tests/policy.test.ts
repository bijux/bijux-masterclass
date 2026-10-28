import assert from 'node:assert/strict'; import test from 'node:test';
import { createDefaultPolicy, createTenantPolicy, decodeOverrides, resolvePolicy } from '../src/index.js';

test('delegates defaults and reports shadowing',()=>{ const d=createDefaultPolicy({maxItems:10,retentionDays:30}); const p=createTenantPolicy(d,'alpha',{maxItems:5}); assert.equal(Object.getPrototypeOf(p),d); assert.deepEqual(resolvePolicy(p,'maxItems'),{value:5,source:'own'}); assert.deepEqual(resolvePolicy(p,'retentionDays'),{value:30,source:'default'}); assert.equal(p.describe(),'alpha: max=5, retention=30'); });

test('decoder ignores inherited input and rejects dangerous own names',()=>{ const inherited=Object.create({maxItems:999}) as object; assert.deepEqual(decodeOverrides(inherited),Object.create(null)); const bad={}; Object.defineProperty(bad,'__proto__',{value:1,enumerable:true}); assert.throws(()=>decodeOverrides(bad),/unsupported/); });

test('frozen inherited defaults reject assignment; explicit construction owns overrides',()=>{ const d=createDefaultPolicy({maxItems:10,retentionDays:30}); const p=createTenantPolicy(d,'beta',{}); assert.equal(Reflect.set(p,'maxItems',7),false); assert.equal(Object.hasOwn(p,'maxItems'),false); const q=createTenantPolicy(d,'gamma',{maxItems:7}); assert.equal(Object.hasOwn(q,'maxItems'),true); assert.equal(q.maxItems,7); assert.equal(d.maxItems,10); });
