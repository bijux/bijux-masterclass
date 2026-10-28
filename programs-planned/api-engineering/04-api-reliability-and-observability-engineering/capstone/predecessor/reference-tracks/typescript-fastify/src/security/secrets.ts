const SENSITIVE = new Set(["authorization","api_key","apikey","password","secret","token","access_token","refresh_token","webhooksecret","webhook_secret","private_key","pepper"]);
const BEARER = /(Bearer)\s+[A-Za-z0-9._~+/-]+/giu;

export class SecretBytes {
  readonly #value: Uint8Array;
  constructor(value: Uint8Array | string) {
    this.#value = typeof value === "string" ? new TextEncoder().encode(value) : new Uint8Array(value);
    if (this.#value.byteLength === 0) throw new Error("secret must not be empty");
  }
  reveal(): Uint8Array { return new Uint8Array(this.#value); }
  toString(): string { return "[REDACTED]"; }
  toJSON(): string { return "[REDACTED]"; }
}

function redactString(value: string): string {
  const bearer = value.replace(BEARER, "$1 [REDACTED]");
  try {
    const url = new URL(bearer);
    if (url.username !== "" || url.password !== "") { url.username = "[REDACTED]"; url.password = ""; return url.toString().replace("%5BREDACTED%5D", "[REDACTED]"); }
  } catch { /* ordinary string */ }
  return bearer;
}

export function redact(value: unknown, key?: string): unknown {
  const normalized = key?.toLowerCase().replaceAll("-", "_");
  if (normalized !== undefined && (SENSITIVE.has(normalized) || SENSITIVE.has(normalized.replaceAll("_", "")))) return "[REDACTED]";
  if (value instanceof SecretBytes) return "[REDACTED]";
  if (Array.isArray(value)) return value.map((item) => redact(item));
  if (value !== null && typeof value === "object") return Object.fromEntries(Object.entries(value as Record<string, unknown>).map(([k,v]) => [k,redact(v,k)]));
  if (typeof value === "string") return redactString(value);
  return value;
}
