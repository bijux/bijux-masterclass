import assert from'node:assert/strict';import test from'node:test';import{createCounter,type Counter}from'../src/index.js';
test('declaration and runtime agree on lifecycle',()=>{const counter:Counter=createCounter(2);assert.equal(counter.increment(3),5);counter.close();assert.throws(()=>counter.value(),/closed/);});
test('runtime rejects values that the number type cannot refine',()=>assert.throws(()=>createCounter(Number.NaN),/safe integer/));
if(false){
  // @ts-expect-error step is numeric
  createCounter().increment('1');
}
