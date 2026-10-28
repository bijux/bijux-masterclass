import assert from'node:assert/strict';import test from'node:test';import{eventName}from'../src/index.js';test('starter derives a name',()=>assert.equal(eventName('name'),'nameChanged'));
