import test from'node:test';import{EventRouter}from'../src/index.js';test('starter registers',()=>new EventRouter().on(()=>undefined));
