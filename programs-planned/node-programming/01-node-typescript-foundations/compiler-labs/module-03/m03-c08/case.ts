function atMost<T>(values: readonly T[], limit: number, visit: (value: T) => boolean): number {
  let calls = 0;
  for (const value of values) {
    if (calls === limit) break;
    calls += 1;
    if (visit(value)) break;
  }
  return calls;
}
console.log(atMost([1, 2, 3], 2, (value) => value === 2));
