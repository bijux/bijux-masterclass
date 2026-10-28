export type Outcome = { readonly kind: 'response'; readonly bytes: Buffer } | { readonly kind: 'timeout'; readonly attempts: number } | { readonly kind: 'socket-error'; readonly code: string };
