import assert from'node:assert/strict';import test from'node:test';import{displayName}from'../src/index.js';test('starter reads a user',()=>assert.equal(displayName({id:'1',name:'Ada'}),'Ada'));
