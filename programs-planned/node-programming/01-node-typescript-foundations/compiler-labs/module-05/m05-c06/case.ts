type State = { kind: 'a' } | { kind: 'b' } | { kind: 'c' };
function unreachable(value: never): never { throw new Error(String(value)); }
function render(state: State): string {
  switch (state.kind) {
    case 'a': return 'A';
    case 'b': return 'B';
    default: return unreachable(state);
  }
}
console.log(render({ kind: 'c' }));
