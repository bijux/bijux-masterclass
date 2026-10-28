function apply(value: number, operation: (input: number) => number): number {
  return operation(value);
}
console.log(apply(3, (value) => value.toString()));
