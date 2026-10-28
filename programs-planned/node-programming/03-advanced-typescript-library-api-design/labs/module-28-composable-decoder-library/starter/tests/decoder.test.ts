import assert from'node:assert/strict';import test from'node:test';import{decodeString}from'../src/index.js';test('starter validates strings',()=>assert.equal(decodeString('x').ok,true));
