import test from 'node:test';
import assert from 'node:assert/strict';
import { wordCount } from '../src/index.js';

test('counts words in a draft', () => assert.equal(wordCount({ state: 'draft', text: 'one two', author: 'A' }), 2));
