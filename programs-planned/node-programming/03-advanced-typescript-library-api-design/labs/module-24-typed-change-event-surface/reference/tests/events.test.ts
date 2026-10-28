import assert from'node:assert/strict';import test from'node:test';import{ChangeStore}from'../src/index.js';
interface Profile{readonly name:string;readonly active:boolean}
test('connects event name to payload',()=>{const store=new ChangeStore<Profile>({name:'Ada',active:false});const seen:string[]=[];const off=store.on('nameChanged',event=>seen.push(`${event.previous}->${event.current}`));store.set('name','Grace');off();store.set('name','Lin');assert.deepEqual(seen,['Ada->Grace']);});
const store=new ChangeStore<Profile>({name:'Ada',active:false});
// @ts-expect-error active events carry booleans, not strings
store.on('activeChanged',(event:{readonly current:string})=>void event);
