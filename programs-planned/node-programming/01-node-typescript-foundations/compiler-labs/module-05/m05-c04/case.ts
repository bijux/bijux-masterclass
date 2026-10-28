function read(value: unknown): string {
  return value.name;
}
console.log(read({ name: 'Node' }));
