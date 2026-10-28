type Result = { kind: 'ok'; text: string } | { kind: 'error'; message: string };
function render(result: Result): string {
  switch (result.kind) {
    case 'ok': return result.text;
    case 'error': return `error: ${result.message}`;
  }
}
console.log(render({ kind: 'ok', text: 'done' }));
