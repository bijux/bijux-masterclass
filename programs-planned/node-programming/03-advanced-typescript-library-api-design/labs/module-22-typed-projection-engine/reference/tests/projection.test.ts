import assert from 'node:assert/strict'; import test from 'node:test'; import { project, select, valuesFor } from '../src/index.js';
const TOKEN=Symbol('token'); const source={name:'Ada',age:37,[TOKEN]:true};
test('preserves key-value and tuple-order relationships',()=>{assert.equal(select(source,TOKEN),true); assert.deepEqual(valuesFor(source,['age','name'] as const),[37,'Ada']); assert.deepEqual(project(source,['name','age'] as const),{name:'Ada',age:37});});
test('rejects duplicate requested keys',()=>assert.throws(()=>project(source,['name','name'] as const),/duplicate/));
// @ts-expect-error source has no role key
select(source,'role');
