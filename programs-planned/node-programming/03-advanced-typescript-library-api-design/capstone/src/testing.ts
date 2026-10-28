import { formatIssues, type ParseResult } from './core.js';

export function expectSuccess<T>(result: ParseResult<T>): T {
  if (!result.ok) throw new Error(`expected success, received:\n${formatIssues(result.issues)}`);
  return result.value;
}

export function expectFailure<T>(result: ParseResult<T>): readonly string[] {
  if (result.ok) throw new Error(`expected failure, received ${JSON.stringify(result.value)}`);
  return result.issues.map((entry) => `${entry.code}@${entry.path.join('.')}`);
}

export type Equal<A, B> =
  (<T>() => T extends A ? 1 : 2) extends
  (<T>() => T extends B ? 1 : 2) ? true : false;

export type Expect<T extends true> = T;
