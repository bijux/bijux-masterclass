function parseCount(raw: string): number {
  if (!/^(0|[1-9]\\d*)$/.test(raw)) throw new Error('invalid count');
  const value = Number(raw);
  if (!Number.isSafeInteger(value)) throw new Error('unsafe count');
  return value;
}
console.log(parseCount('12'));
