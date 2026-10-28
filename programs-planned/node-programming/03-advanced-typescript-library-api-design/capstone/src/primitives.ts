import { internalSchema, issue, success, type Schema } from './core.js';

export function string(): Schema<string> {
  return internalSchema('string', (input, path) =>
    typeof input === 'string' ? success(input) : issue(path, 'type.string', 'expected a string'));
}

export function boolean(): Schema<boolean> {
  return internalSchema('boolean', (input, path) =>
    typeof input === 'boolean' ? success(input) : issue(path, 'type.boolean', 'expected a Boolean'));
}

export function number(): Schema<number> {
  return internalSchema('number', (input, path) =>
    typeof input === 'number' && Number.isFinite(input)
      ? success(input)
      : issue(path, 'type.number', 'expected a finite number'));
}

export type Literal = string | number | boolean | null;

export function literal<const V extends Literal>(expected: V): Schema<V> {
  return internalSchema(`literal(${String(expected)})`, (input, path) =>
    Object.is(input, expected)
      ? success(expected)
      : issue(path, 'literal.mismatch', `expected ${JSON.stringify(expected)}`));
}

export function unknown(): Schema<unknown> {
  return internalSchema('unknown', (input) => success(input));
}
