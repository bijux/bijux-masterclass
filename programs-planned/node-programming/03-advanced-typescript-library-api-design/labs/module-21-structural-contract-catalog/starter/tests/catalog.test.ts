import assert from 'node:assert/strict'; import test from 'node:test';
import { listFeatureIds } from '../src/index.js';
test('starter preserves source order',()=>assert.deepEqual(listFeatureIds([{id:'search',label:'Search'}]),['search']));
