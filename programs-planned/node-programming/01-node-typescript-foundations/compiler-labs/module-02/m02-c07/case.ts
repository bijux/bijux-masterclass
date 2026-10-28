function render(input: string | number): string {
  if (input) {
    const text: string = input;
    return text;
  }
  return 'empty';
}
console.log(render(1));
