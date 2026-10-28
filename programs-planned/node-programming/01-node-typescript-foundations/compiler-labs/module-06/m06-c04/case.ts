const rows = [{ id: 1, name: 'A' }, { id: 1, name: 'B' }];
const index = new Map<number, string>();
for (const row of rows) {
  if (index.has(row.id)) throw new Error(`duplicate ${row.id}`);
  index.set(row.id, row.name);
}
