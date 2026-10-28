type Input = { kind: 'text'; value: string } | { kind: 'count'; value: number };
function render(input: Input): string {
  switch (input.kind) {
    case 'text': return input.value;
    case 'count': return input.value.toString();
  }
}
console.log(render({ kind: 'count', value: 3 }));
