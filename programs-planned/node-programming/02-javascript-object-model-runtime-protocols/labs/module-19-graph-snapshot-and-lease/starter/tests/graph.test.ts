import assert from 'node:assert/strict'; import test from 'node:test'; import { createNode } from '../src/index.js';
test('baseline creates independent nodes',()=>{const a=createNode('a','A'),b=createNode('b','B');a.edges.push(b);assert.equal(a.edges[0],b);});
