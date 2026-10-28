const original = { supplier: { email: 'a@example.test' } };
const copy = { ...original };
copy.supplier.email = 'b@example.test';
if (original.supplier.email !== 'a@example.test') throw new Error('original changed');
