import assert from'node:assert/strict';import test from'node:test';import{array,field,finite,text,type Output}from'../src/index.js';
test('composes path-aware decoders',()=>{const names=array(text());const failed=names.decode(['Ada',2]);assert.equal(failed.ok,false);if(!failed.ok)assert.deepEqual(failed.issues[0]?.path,[1]);assert.deepEqual(field('age',finite()).decode({age:37}),{ok:true,value:{age:37}});});
const Age=field('age',finite());type Age=Output<typeof Age>;const value:Age={age:2};void value;
// @ts-expect-error age output is numeric
const invalid:Age={age:'2'};void invalid;
