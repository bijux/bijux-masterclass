function first<T>(values: readonly T[], accept: (value: T) => boolean): T | undefined {
  return values.find(accept);
}
const found = first(['node', 'ts'], (value) => value.length === 2);
console.log(found ?? 'missing');
