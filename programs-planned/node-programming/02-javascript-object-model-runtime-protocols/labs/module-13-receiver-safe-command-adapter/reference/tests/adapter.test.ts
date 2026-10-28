import assert from 'node:assert/strict'; import test from 'node:test'; import { adaptMethod, CommandRegistry, constructWith } from '../src/index.js';
class Service { calls=0; constructor(readonly prefix:string){} execute(this:Service,value:string):string{this.calls+=1;return `${this.prefix}:${value}`;} }
class Box { constructor(readonly value:number){} }

test('adapter preserves exact receiver and call count',()=>{ const s=new Service('p'); const raw=s.execute; assert.throws(()=>Reflect.apply(raw,undefined,['x'])); const r=new CommandRegistry(); r.register('run',adaptMethod(s,s.execute)); assert.equal(r.invoke<string>('run','x'),'p:x'); assert.equal(s.calls,1); });

test('registry preserves domain failure and rejects duplicates',()=>{ const r=new CommandRegistry(); const error=new Error('domain'); r.register('fail',()=>{throw error;}); assert.throws(()=>r.invoke('fail'),(caught)=>caught===error); assert.throws(()=>r.register('fail',()=>1)); });

test('construction is a distinct operation',()=>{ const b=constructWith(Box,[4] as const); assert.equal(b.value,4); assert.throws(()=>Reflect.construct((()=>1),[])); });
