type Result = { kind: 'committed' } | { kind: 'rejected' };
function render(result: Result): string { if (result.kind === 'committed') return 'ok'; const impossible: never = result; return impossible; }
void render;
