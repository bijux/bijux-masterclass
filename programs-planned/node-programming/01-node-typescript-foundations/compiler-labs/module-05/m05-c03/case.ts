function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
const input: unknown = { name: 'Node' };
if (!isRecord(input) || typeof input['name'] !== 'string') throw new Error('invalid');
console.log(input['name'].toUpperCase());
