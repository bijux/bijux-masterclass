import { parseArgs } from 'node:util';
import { CommandError } from './errors.js';
import type { SessionStatus } from './domain.js';

export type Command =
  | { readonly kind: 'plan'; readonly topic: string; readonly minutes: number }
  | { readonly kind: 'start'; readonly id: number }
  | { readonly kind: 'complete'; readonly id: number; readonly minutes: number; readonly note?: string }
  | { readonly kind: 'abandon'; readonly id: number; readonly reason: string }
  | { readonly kind: 'list'; readonly status?: SessionStatus }
  | { readonly kind: 'show'; readonly id: number }
  | { readonly kind: 'search'; readonly query: string }
  | { readonly kind: 'summary' }
  | { readonly kind: 'help' }
  | { readonly kind: 'version' };

interface ParsedOptions {
  readonly values: Record<string, string | boolean | undefined>;
  readonly positionals: readonly string[];
}

function parseSubcommand(
  args: readonly string[],
  options: Readonly<Record<string, { readonly type: 'string' | 'boolean' }>>,
): ParsedOptions {
  try {
    const parsed = parseArgs({
      args: [...args],
      options,
      strict: true,
      allowPositionals: true,
      tokens: true,
    });
    const seen = new Set<string>();
    for (const token of parsed.tokens) {
      if (token.kind !== 'option') continue;
      if (seen.has(token.name)) throw new CommandError(`option --${token.name} may appear only once`);
      seen.add(token.name);
    }
    return { values: parsed.values, positionals: parsed.positionals };
  } catch (error: unknown) {
    if (error instanceof CommandError) throw error;
    throw new CommandError(error instanceof Error ? error.message : 'invalid command arguments', { cause: error });
  }
}

function requiredString(value: string | boolean | undefined, option: string): string {
  if (typeof value !== 'string') throw new CommandError(`missing required option --${option}`);
  return value;
}

function parsePositiveInteger(raw: string, label: string): number {
  if (!/^(0|[1-9]\d*)$/u.test(raw)) throw new CommandError(`${label} must contain decimal digits only`);
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value <= 0) throw new CommandError(`${label} must be a positive safe integer`);
  return value;
}

function exactly(positionals: readonly string[], count: number, usage: string): void {
  if (positionals.length !== count) throw new CommandError(`usage: ${usage}`);
}

function parseStatus(value: string | boolean | undefined): SessionStatus | undefined {
  if (value === undefined) return undefined;
  if (value === 'planned' || value === 'active' || value === 'completed' || value === 'abandoned') return value;
  throw new CommandError('--status must be planned, active, completed, or abandoned');
}

export function parseCommand(argv: readonly string[]): Command {
  const [name, ...tail] = argv;
  switch (name) {
    case undefined:
    case 'help': {
      exactly(tail, 0, 'studyledger help');
      return { kind: 'help' };
    }
    case 'version': {
      exactly(tail, 0, 'studyledger version');
      return { kind: 'version' };
    }
    case 'plan': {
      const parsed = parseSubcommand(tail, { topic: { type: 'string' }, minutes: { type: 'string' } });
      exactly(parsed.positionals, 0, 'studyledger plan --topic <text> --minutes <integer>');
      return {
        kind: 'plan',
        topic: requiredString(parsed.values['topic'], 'topic'),
        minutes: parsePositiveInteger(requiredString(parsed.values['minutes'], 'minutes'), 'minutes'),
      };
    }
    case 'start': {
      const parsed = parseSubcommand(tail, {});
      exactly(parsed.positionals, 1, 'studyledger start <id>');
      const rawId = parsed.positionals[0];
      if (rawId === undefined) throw new CommandError('missing session id');
      return { kind: 'start', id: parsePositiveInteger(rawId, 'id') };
    }
    case 'complete': {
      const parsed = parseSubcommand(tail, { minutes: { type: 'string' }, note: { type: 'string' } });
      exactly(parsed.positionals, 1, 'studyledger complete <id> --minutes <integer> [--note <text>]');
      const rawId = parsed.positionals[0];
      if (rawId === undefined) throw new CommandError('missing session id');
      const note = parsed.values['note'];
      return note === undefined
        ? {
            kind: 'complete',
            id: parsePositiveInteger(rawId, 'id'),
            minutes: parsePositiveInteger(requiredString(parsed.values['minutes'], 'minutes'), 'minutes'),
          }
        : {
            kind: 'complete',
            id: parsePositiveInteger(rawId, 'id'),
            minutes: parsePositiveInteger(requiredString(parsed.values['minutes'], 'minutes'), 'minutes'),
            note: requiredString(note, 'note'),
          };
    }
    case 'abandon': {
      const parsed = parseSubcommand(tail, { reason: { type: 'string' } });
      exactly(parsed.positionals, 1, 'studyledger abandon <id> --reason <text>');
      const rawId = parsed.positionals[0];
      if (rawId === undefined) throw new CommandError('missing session id');
      return {
        kind: 'abandon',
        id: parsePositiveInteger(rawId, 'id'),
        reason: requiredString(parsed.values['reason'], 'reason'),
      };
    }
    case 'list': {
      const parsed = parseSubcommand(tail, { status: { type: 'string' } });
      exactly(parsed.positionals, 0, 'studyledger list [--status <status>]');
      const status = parseStatus(parsed.values['status']);
      return status === undefined ? { kind: 'list' } : { kind: 'list', status };
    }
    case 'show': {
      const parsed = parseSubcommand(tail, {});
      exactly(parsed.positionals, 1, 'studyledger show <id>');
      const rawId = parsed.positionals[0];
      if (rawId === undefined) throw new CommandError('missing session id');
      return { kind: 'show', id: parsePositiveInteger(rawId, 'id') };
    }
    case 'search': {
      const parsed = parseSubcommand(tail, { query: { type: 'string' } });
      exactly(parsed.positionals, 0, 'studyledger search --query <text>');
      return { kind: 'search', query: requiredString(parsed.values['query'], 'query') };
    }
    case 'summary': {
      const parsed = parseSubcommand(tail, {});
      exactly(parsed.positionals, 0, 'studyledger summary');
      return { kind: 'summary' };
    }
    default:
      throw new CommandError(`unknown command: ${name}`);
  }
}
