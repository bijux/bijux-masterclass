import assert from'node:assert/strict';import test from'node:test';import{EventRouter}from'../src/index.js';
interface Events{readonly message:{readonly text:string};readonly count:{readonly value:number}}
test('uses snapshot dispatch and idempotent unsubscribe',()=>{const router=new EventRouter<Events>();const seen:string[]=[];let off:()=>void=()=>undefined;off=router.on('message',value=>{seen.push(value.text);off();});router.emit('message',{text:'one'});router.emit('message',{text:'two'});off();assert.deepEqual(seen,['one']);});
const router=new EventRouter<Events>();
// @ts-expect-error payload does not satisfy count event
router.emit('count',{text:'wrong'});
