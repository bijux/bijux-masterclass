const item = { id: 1, supplier: { name: 'A', email: 'a@example.test' } };
const updated = { ...item, supplier: { ...item.supplier, email: 'b@example.test' } };
console.log(item !== updated, item.supplier !== updated.supplier);
