export type PathSegment = string | number;

export interface Issue {
  readonly path: readonly PathSegment[];
  readonly code: string;
  readonly message: string;
}

export type ParseResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly issues: readonly [Issue, ...Issue[]] };

export interface Schema<out T> {
  readonly kind: string;
  safeParse(input: unknown): ParseResult<T>;
  parse(input: unknown): T;
}

export type Infer<S extends Schema<unknown>> = S extends Schema<infer T> ? T : never;

export class SchemaError extends Error {
  readonly issues: readonly [Issue, ...Issue[]];

  constructor(issues: readonly [Issue, ...Issue[]]) {
    super(formatIssues(issues));
    this.name = 'SchemaError';
    this.issues = issues;
  }
}

export const MAX_ISSUES = 64;

export interface IssueBudget {
  readonly max: number;
}

export type Decoder<T> = (
  input: unknown,
  path: readonly PathSegment[],
  budget: IssueBudget,
) => ParseResult<T>;

const DECODER = Symbol('schemakit.decoder');
type InternalSchema<T> = Schema<T> & { readonly [DECODER]: Decoder<T> };

export function success<T>(value: T): ParseResult<T> {
  return { ok: true, value };
}

export function failure(issue: Issue): ParseResult<never> {
  return { ok: false, issues: [issue] };
}

export function issuesFailure(issues: readonly Issue[]): ParseResult<never> {
  const first = issues[0];
  if (first === undefined) throw new Error('a failed parse must contain at least one issue');
  return { ok: false, issues: [first, ...issues.slice(1)] };
}

export function issue(
  path: readonly PathSegment[],
  code: string,
  message: string,
): ParseResult<never> {
  return failure({ path: [...path], code, message });
}

export function internalSchema<T, E extends object = Record<never, never>>(
  kind: string,
  decode: Decoder<T>,
  extras?: E,
): Schema<T> & E {
  const value = Object.assign({
    kind,
    safeParse(input: unknown): ParseResult<T> {
      return decode(input, [], { max: MAX_ISSUES });
    },
    parse(input: unknown): T {
      const result = decode(input, [], { max: MAX_ISSUES });
      if (result.ok) return result.value;
      throw new SchemaError(result.issues);
    },
    [DECODER]: decode,
  }, extras ?? {}) as InternalSchema<T> & E;
  return Object.freeze(value);
}

export function decodeWith<T>(
  schema: Schema<T>,
  input: unknown,
  path: readonly PathSegment[],
  budget: IssueBudget,
): ParseResult<T> {
  const decoder = (schema as InternalSchema<T>)[DECODER];
  if (decoder === undefined) {
    const result = schema.safeParse(input);
    if (result.ok || path.length === 0) return result;
    return issuesFailure(result.issues.map((entry) => ({ ...entry, path: [...path, ...entry.path] })));
  }
  return decoder(input, path, budget);
}

export function formatPath(path: readonly PathSegment[]): string {
  if (path.length === 0) return '$';
  return path.reduce<string>((result, segment) =>
    typeof segment === 'number'
      ? `${result}[${segment}]`
      : /^[A-Za-z_$][\w$]*$/.test(segment)
        ? `${result}.${segment}`
        : `${result}[${JSON.stringify(segment)}]`, '$');
}

export function formatIssues(issues: readonly Issue[]): string {
  return issues.map((entry) => `${formatPath(entry.path)}: ${entry.message} (${entry.code})`).join('\n');
}
