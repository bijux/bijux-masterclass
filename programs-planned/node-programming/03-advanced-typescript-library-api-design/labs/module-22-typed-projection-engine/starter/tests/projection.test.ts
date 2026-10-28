import assert from 'node:assert/strict'; import test from 'node:test'; import { select } from '../src/index.js';
test('starter selects a known key',()=>assert.equal(select({name:'Ada'},'name'),'Ada'));
