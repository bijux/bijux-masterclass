import assert from'node:assert/strict';import test from'node:test';import{greet}from'../src/index.js';test('starter exports one function',()=>assert.equal(greet('Ada'),'Hello, Ada'));
