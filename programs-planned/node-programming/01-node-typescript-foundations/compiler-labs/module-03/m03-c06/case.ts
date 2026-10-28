function read(this: { readonly value: number }): number {
  return this.value;
}
console.log(read.call({ value: 9 }));
