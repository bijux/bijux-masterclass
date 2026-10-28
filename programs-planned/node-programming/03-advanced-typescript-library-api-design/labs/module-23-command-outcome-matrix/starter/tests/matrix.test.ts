import assert from 'node:assert/strict';import test from 'node:test';import{commandKind}from'../src/index.js';test('starter identifies commands',()=>assert.equal(commandKind({kind:'ping'}),'ping'));
