export interface Supplier {
  readonly name: string;
  readonly email: string;
}

export interface Item {
  readonly id: number;
  readonly name: string;
  readonly stock: number;
  readonly supplier: Supplier;
}

export interface Inventory {
  readonly items: readonly Item[];
}

function updateItem(inventory: Inventory, id: number, update: (item: Item) => Item): Inventory {
  let found = false;
  const items = inventory.items.map((item) => {
    if (item.id !== id) return item;
    found = true;
    return update(item);
  });
  if (!found) throw new Error(`missing item ${id}`);
  return { items };
}

export function renameItem(inventory: Inventory, id: number, rawName: string): Inventory {
  const name = rawName.trim();
  if (name.length === 0) throw new Error('name must not be empty');
  return updateItem(inventory, id, (item) => ({ ...item, name }));
}

export function adjustStock(inventory: Inventory, id: number, delta: number): Inventory {
  if (!Number.isSafeInteger(delta)) throw new Error('delta must be a safe integer');
  return updateItem(inventory, id, (item) => {
    const stock = item.stock + delta;
    if (!Number.isSafeInteger(stock) || stock < 0) throw new Error('stock would be invalid');
    return { ...item, stock };
  });
}

export function updateSupplierEmail(inventory: Inventory, id: number, rawEmail: string): Inventory {
  const email = rawEmail.trim();
  if (!/^[^\s@]+@[^\s@]+$/.test(email)) throw new Error('invalid supplier email');
  return updateItem(inventory, id, (item) => ({ ...item, supplier: { ...item.supplier, email } }));
}

export function totalStock(inventory: Inventory): number {
  return inventory.items.reduce((sum, item) => sum + item.stock, 0);
}
