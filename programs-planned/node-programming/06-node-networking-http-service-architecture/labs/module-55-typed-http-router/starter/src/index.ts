export type Route =
  | { readonly kind: 'health' }
  | { readonly kind: 'submit' }
  | { readonly kind: 'job'; readonly id: string }
  | { readonly kind: 'not-found' };

export function matchRoute(method: string, url: URL): Route {
  if (method === 'GET' && url.pathname === '/health') return { kind: 'health' };
  if (method === 'POST' && url.pathname === '/jobs') return { kind: 'submit' };
  const match = /^\/jobs\/([A-Za-z0-9-]+)$/.exec(url.pathname);
  if (method === 'GET' && match?.[1]) return { kind: 'job', id: match[1] };
  return { kind: 'not-found' };
}
