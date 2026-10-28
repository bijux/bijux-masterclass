export interface Item {
  readonly id: number;
  readonly name: string;
  readonly stock: number;
}

export interface Inventory {
  readonly items: readonly Item[];
}

export function totalStock(inventory: Inventory): number {
  return inventory.items.reduce((sum, item) => sum + item.stock, 0);
}
