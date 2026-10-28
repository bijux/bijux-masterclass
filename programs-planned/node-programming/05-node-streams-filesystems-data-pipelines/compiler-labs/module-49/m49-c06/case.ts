type Outcome = { kind: 'committed'; bytes: number } | { kind: 'failed'; message: string };
function render(value: Outcome): string { if (value.kind === 'committed') return String(value.bytes); }
void render;
