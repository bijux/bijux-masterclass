interface Request { readonly nonce: string }
export function rewrite(request: Request): void { request.nonce = 'other'; }
