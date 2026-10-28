import assert from'node:assert/strict';import test from'node:test';import{total}from'../src/index.js';test('starter totals records',()=>assert.equal(total([{id:'a',score:2}]),2));
