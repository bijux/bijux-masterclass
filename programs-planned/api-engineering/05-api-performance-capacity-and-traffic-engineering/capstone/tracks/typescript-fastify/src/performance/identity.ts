import { createHash } from "node:crypto";

export class IdentityError extends Error {}

type JSONValue =
  | null
  | boolean
  | number
  | string
  | JSONValue[]
  | { [key: string]: JSONValue };

function normalize(value: unknown): JSONValue {
  if (
    value === null ||
    typeof value === "string" ||
    typeof value === "boolean"
  ) {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new IdentityError("non-finite numbers are forbidden");
    }
    if (Number.isInteger(value) && !Number.isSafeInteger(value)) {
      throw new IdentityError("unsafe integers are forbidden");
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.map(normalize);
  }
  if (typeof value === "object") {
    const source = value as Record<string, unknown>;
    const output: Record<string, JSONValue> = {};
    for (const key of Object.keys(source).sort()) {
      if (key === "__proto__" || key === "constructor" || key === "prototype") {
        throw new IdentityError("prototype-sensitive key is forbidden");
      }
      output[key] = normalize(source[key]);
    }
    return output;
  }
  throw new IdentityError(`unsupported identity value: ${typeof value}`);
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(normalize(value));
}

export function sha256Identity(value: unknown): string {
  return `sha256:${createHash("sha256").update(canonicalJson(value)).digest("hex")}`;
}
