import test from 'node:test';
import assert from 'node:assert/strict';
import { adjustStock, renameItem, updateSupplierEmail, type Inventory } from '../src/index.js';

const source = (): Inventory => ({ items: [
  { id: 1, name: 'paper', stock: 3, supplier: { name: 'A', email: 'a@example.test' } },
  { id: 2, name: 'ink', stock: 4, supplier: { name: 'B', email: 'b@example.test' } },
] });

test('copies only the changed path', () => {
  const before = source();
  const after = updateSupplierEmail(before, 1, 'new@example.test');
  assert.notEqual(after, before);
  assert.notEqual(after.items, before.items);
  assert.notEqual(after.items[0], before.items[0]);
  assert.notEqual(after.items[0]?.supplier, before.items[0]?.supplier);
  assert.equal(after.items[1], before.items[1]);
  assert.equal(before.items[0]?.supplier.email, 'a@example.test');
});

test('failure leaves source unchanged', () => {
  const before = source();
  assert.throws(() => adjustStock(before, 1, -10));
  assert.equal(before.items[0]?.stock, 3);
});

test('renames canonically', () => {
  assert.equal(renameItem(source(), 2, '  toner ').items[1]?.name, 'toner');
});
