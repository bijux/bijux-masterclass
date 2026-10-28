function validate(value: unknown): readonly string[] {
  const issues: string[] = [];
  if (typeof value !== 'object' || value === null) return ['expected object'];
  if (!('name' in value) || typeof value.name !== 'string') issues.push('invalid name');
  if (!('count' in value) || typeof value.count !== 'number') issues.push('invalid count');
  return issues;
}
console.log(validate({ name: 1, count: 'x' }).length);
