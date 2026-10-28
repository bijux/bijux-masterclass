export class UsageError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'UsageError';
  }
}

export type Command =
  | { readonly kind: 'help' }
  | { readonly kind: 'version' }
  | { readonly kind: 'demo' }
  | {
      readonly kind: 'serve';
      readonly host: string;
      readonly port: number;
      readonly http2Port?: number;
      readonly discoveryPort?: number;
    }
  | {
      readonly kind: 'submit';
      readonly baseUrl: URL;
      readonly idempotencyKey: string;
      readonly operation: 'uppercase' | 'word-count' | 'checksum' | 'sleep';
      readonly payload: string;
    }
  | { readonly kind: 'get'; readonly baseUrl: URL; readonly id: string }
  | { readonly kind: 'stats'; readonly baseUrl: URL }
  | { readonly kind: 'discover'; readonly host: string; readonly port: number };

function parsePort(text: string, label: string): number {
  const value = Number(text);
  if (!Number.isInteger(value) || value < 0 || value > 65_535) {
    throw new UsageError(`${label} must be an integer between 0 and 65535`);
  }
  return value;
}

function takeValue(args: string[], name: string): string | undefined {
  const index = args.indexOf(name);
  if (index < 0) return undefined;
  const value = args[index + 1];
  if (value === undefined) throw new UsageError(`${name} requires a value`);
  args.splice(index, 2);
  return value;
}

function assertNoExtras(args: readonly string[]): void {
  if (args.length > 0) throw new UsageError(`unexpected arguments: ${args.join(' ')}`);
}

function parseBaseUrl(text: string | undefined): URL {
  if (!text) throw new UsageError('--url is required');
  let url: URL;
  try { url = new URL(text); } catch { throw new UsageError('--url must be an absolute URL'); }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new UsageError('--url must use http or https');
  }
  return url;
}

export function parseCommand(argv: readonly string[]): Command {
  const [name, ...rest] = argv;
  if (!name || name === 'help' || name === '--help') return { kind: 'help' };
  if (name === 'version' || name === '--version') return { kind: 'version' };
  if (name === 'demo') {
    assertNoExtras(rest);
    return { kind: 'demo' };
  }
  if (name === 'serve') {
    const args = [...rest];
    const host = takeValue(args, '--host') ?? '127.0.0.1';
    const port = parsePort(takeValue(args, '--port') ?? '8080', '--port');
    const h2 = takeValue(args, '--http2-port');
    const discovery = takeValue(args, '--discovery-port');
    assertNoExtras(args);
    return {
      kind: 'serve',
      host,
      port,
      ...(h2 !== undefined ? { http2Port: parsePort(h2, '--http2-port') } : {}),
      ...(discovery !== undefined ? { discoveryPort: parsePort(discovery, '--discovery-port') } : {}),
    };
  }
  if (name === 'submit') {
    const args = [...rest];
    const baseUrl = parseBaseUrl(takeValue(args, '--url'));
    const idempotencyKey = takeValue(args, '--key');
    const operation = takeValue(args, '--operation');
    const payload = takeValue(args, '--payload');
    assertNoExtras(args);
    if (!idempotencyKey || !/^[A-Za-z0-9._:-]{8,128}$/.test(idempotencyKey)) {
      throw new UsageError('--key must contain 8–128 allowed characters');
    }
    if (operation !== 'uppercase' && operation !== 'word-count' && operation !== 'checksum' && operation !== 'sleep') {
      throw new UsageError('--operation must be uppercase, word-count, checksum, or sleep');
    }
    if (payload === undefined) throw new UsageError('--payload is required');
    return { kind: 'submit', baseUrl, idempotencyKey, operation, payload };
  }
  if (name === 'get') {
    const args = [...rest];
    const baseUrl = parseBaseUrl(takeValue(args, '--url'));
    const id = args.shift();
    if (!id) throw new UsageError('get requires <job-id>');
    assertNoExtras(args);
    return { kind: 'get', baseUrl, id };
  }
  if (name === 'stats') {
    const args = [...rest];
    const baseUrl = parseBaseUrl(takeValue(args, '--url'));
    assertNoExtras(args);
    return { kind: 'stats', baseUrl };
  }
  if (name === 'discover') {
    const args = [...rest];
    const host = takeValue(args, '--host') ?? '127.0.0.1';
    const portText = takeValue(args, '--port');
    if (!portText) throw new UsageError('discover requires --port');
    assertNoExtras(args);
    return { kind: 'discover', host, port: parsePort(portText, '--port') };
  }
  throw new UsageError(`unknown command: ${name}`);
}
