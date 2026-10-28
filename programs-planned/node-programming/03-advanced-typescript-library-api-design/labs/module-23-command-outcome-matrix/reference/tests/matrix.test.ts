import assert from'node:assert/strict';import test from'node:test';import{execute,type Outcome}from'../src/index.js';
test('computes runtime outcomes',()=>{assert.equal(execute({kind:'ping'}),'pong');assert.equal(execute({kind:'length',text:'abc'}),3);assert.deepEqual(execute({kind:'divide',numerator:4,denominator:0}),{ok:false,reason:'division-by-zero'});});
const lengthResult:Outcome<{readonly kind:'length';readonly text:string}>=3;void lengthResult;
// @ts-expect-error ping outcome is not numeric
const invalid:Outcome<{readonly kind:'ping'}>=3;void invalid;
