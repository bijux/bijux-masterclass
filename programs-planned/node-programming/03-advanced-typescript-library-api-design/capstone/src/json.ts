import type { ParseResult, Schema } from './core.js';

export type JsonValue =
  | null
  | boolean
  | number
  | string
  | readonly JsonValue[]
  | { readonly [key: string]: JsonValue };

export class JsonSyntaxError extends Error {
  readonly sourceName: string;
  constructor(sourceName: string, message: string) {
    super(`${sourceName}: ${message}`);
    this.name = 'JsonSyntaxError';
    this.sourceName = sourceName;
  }
}

export function parseJson(text: string, sourceName = '<json>'): unknown {
  try {
    return JSON.parse(text) as unknown;
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'invalid JSON';
    throw new JsonSyntaxError(sourceName, message);
  }
}

export function parseJsonWith<T>(schema: Schema<T>, text: string, sourceName = '<json>'): T {
  return schema.parse(parseJson(text, sourceName));
}

export function safeParseJsonWith<T>(
  schema: Schema<T>,
  text: string,
  sourceName = '<json>',
): ParseResult<T> | { readonly ok: false; readonly syntax: JsonSyntaxError } {
  try {
    return schema.safeParse(parseJson(text, sourceName));
  } catch (error: unknown) {
    if (error instanceof JsonSyntaxError) return { ok: false, syntax: error };
    throw error;
  }
}

export function canonicalJson(value: unknown): string {
  return `${JSON.stringify(sortJson(value), null, 2)}\n`;
}

function sortJson(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortJson);
  if (typeof value === 'object' && value !== null) {
    const output: Record<string, unknown> = {};
    for (const key of Object.keys(value).sort()) output[key] = sortJson(Reflect.get(value, key));
    return output;
  }
  return value;
}
