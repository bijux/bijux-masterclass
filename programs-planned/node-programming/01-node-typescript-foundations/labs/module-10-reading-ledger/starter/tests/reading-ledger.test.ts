import test from 'node:test';
import assert from 'node:assert/strict';
import { queueBook } from '../src/index.js';

test('queues a normalized title', () => assert.deepEqual(queueBook(1, '  Book  '), { state: 'queued', id: 1, title: 'Book' }));
