export class CanonicalizationError extends Error {}

const MAX_SAFE = Number.MAX_SAFE_INTEGER;

function validate(value: unknown, path = "$"): void {
  if (value === null || typeof value === "string" || typeof value === "boolean") return;
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new CanonicalizationError(`non-finite number at ${path}`);
    if (!Number.isInteger(value)) {
      throw new CanonicalizationError(`floating-point number at ${path}; use a scaled integer or decimal string`);
    }
    if (Math.abs(value) > MAX_SAFE) throw new CanonicalizationError(`unsafe integer at ${path}`);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => validate(item, `${path}[${index}]`));
    return;
  }
  if (typeof value === "object") {
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
      validate(item, `${path}.${key}`);
    }
    return;
  }
  throw new CanonicalizationError(`unsupported value ${typeof value} at ${path}`);
}

function normalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(normalize);
  if (value !== null && typeof value === "object") {
    const result: Record<string, unknown> = {};
    for (const key of Object.keys(value as Record<string, unknown>).sort()) {
      result[key] = normalize((value as Record<string, unknown>)[key]);
    }
    return result;
  }
  return value;
}

export function canonicalJson(value: unknown): string {
  validate(value);
  return JSON.stringify(normalize(value));
}

export function canonicalBytes(value: unknown): Uint8Array {
  return new TextEncoder().encode(canonicalJson(value));
}
