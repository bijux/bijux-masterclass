import test from 'node:test';
import assert from 'node:assert/strict';
import { renderEntries } from '../src/index.js';

test('renders deterministic supplied order', () => assert.equal(renderEntries([{ name: 'a', size: 2 }]), 'a\t2\n'));
