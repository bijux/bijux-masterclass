type Result = { readonly kind: 'committed'; readonly path: string } | { readonly kind: 'rejected'; readonly reason: string };
function render(result: Result): string { return result.kind === 'committed' ? result.path : result.reason; }
void render;
