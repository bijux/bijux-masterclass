import assert from 'node:assert/strict'; import test from 'node:test'; import { Hierarchy, TraversalInvalidatedError } from '../src/index.js';
const nodes=[{id:'a',children:['b','c']},{id:'b',children:['d']},{id:'c',children:[]},{id:'d',children:[]}];
test('supports three deterministic orders',()=>{const h=new Hierarchy(nodes,['a']);assert.deepEqual([...h],['a','b','d','c']);assert.deepEqual([...h.postorder()],['d','b','c','a']);assert.deepEqual([...h.breadth()],['a','b','c','d']);});
test('early close and mutation are observable',()=>{const h=new Hierarchy(nodes,['a']);for(const id of h){assert.equal(id,'a');break;}assert.equal(h.closedTraversals,1);const it=h.preorder();assert.deepEqual(it.next(),{value:'a',done:false});h.replace({id:'c',children:[]});assert.throws(()=>it.next(),TraversalInvalidatedError);});
test('rejects cycles',()=>{assert.throws(()=>new Hierarchy([{id:'a',children:['b']},{id:'b',children:['a']}],['a']),/cycle/);});
