import { SecurityControlError } from "./errors.js";

const DANGEROUS_KEYS = new Set(["__proto__", "prototype", "constructor"]);

type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

class Parser {
  private index = 0;
  constructor(private readonly text: string, private readonly maxDepth: number) {}

  parse(): JsonValue {
    this.skipWhitespace();
    const value = this.parseValue(1);
    this.skipWhitespace();
    if (this.index !== this.text.length) {
      throw new SecurityControlError("trailing-content", "content follows the JSON value");
    }
    return value;
  }

  private parseValue(depth: number): JsonValue {
    if (depth > this.maxDepth) {
      throw new SecurityControlError("depth", "JSON nesting exceeds the configured maximum");
    }
    this.skipWhitespace();
    const ch = this.text[this.index];
    if (ch === '"') return this.parseString();
    if (ch === "{") return this.parseObject(depth);
    if (ch === "[") return this.parseArray(depth);
    if (ch === "t") return this.literal("true", true);
    if (ch === "f") return this.literal("false", false);
    if (this.text.startsWith("NaN", this.index)) throw new SecurityControlError("non-finite", "JSON number is not finite");
    if (ch === "n") return this.literal("null", null);
    if (this.text.startsWith("Infinity", this.index) || this.text.startsWith("-Infinity", this.index)) throw new SecurityControlError("non-finite", "JSON number is not finite");
    if (ch === "-" || (ch !== undefined && ch >= "0" && ch <= "9")) return this.parseNumber();
    throw new SecurityControlError("invalid-json", "JSON syntax is invalid");
  }

  private parseObject(depth: number): { [key: string]: JsonValue } {
    this.index += 1;
    const result: { [key: string]: JsonValue } = Object.create(null) as { [key: string]: JsonValue };
    const seen = new Set<string>();
    this.skipWhitespace();
    if (this.text[this.index] === "}") { this.index += 1; return result; }
    while (true) {
      this.skipWhitespace();
      if (this.text[this.index] !== '"') throw new SecurityControlError("invalid-json", "object member name is invalid");
      const key = this.parseString();
      if (seen.has(key)) throw new SecurityControlError("duplicate-key", "JSON object contains a duplicate member");
      if (DANGEROUS_KEYS.has(key)) throw new SecurityControlError("dangerous-key", "JSON object contains a prohibited member name");
      seen.add(key);
      this.skipWhitespace();
      if (this.text[this.index] !== ":") throw new SecurityControlError("invalid-json", "object member separator is missing");
      this.index += 1;
      result[key] = this.parseValue(depth + 1);
      this.skipWhitespace();
      const delimiter = this.text[this.index];
      if (delimiter === "}") { this.index += 1; return result; }
      if (delimiter !== ",") throw new SecurityControlError("invalid-json", "object delimiter is invalid");
      this.index += 1;
    }
  }

  private parseArray(depth: number): JsonValue[] {
    this.index += 1;
    const result: JsonValue[] = [];
    this.skipWhitespace();
    if (this.text[this.index] === "]") { this.index += 1; return result; }
    while (true) {
      result.push(this.parseValue(depth + 1));
      this.skipWhitespace();
      const delimiter = this.text[this.index];
      if (delimiter === "]") { this.index += 1; return result; }
      if (delimiter !== ",") throw new SecurityControlError("invalid-json", "array delimiter is invalid");
      this.index += 1;
    }
  }

  private parseString(): string {
    const start = this.index;
    this.index += 1;
    while (this.index < this.text.length) {
      const ch = this.text[this.index];
      if (ch === '"') {
        this.index += 1;
        const raw = this.text.slice(start, this.index);
        try { return JSON.parse(raw) as string; }
        catch { throw new SecurityControlError("invalid-json", "JSON string is invalid"); }
      }
      if (ch === "\\") {
        this.index += 2;
        continue;
      }
      if (ch !== undefined && ch.charCodeAt(0) < 0x20) throw new SecurityControlError("invalid-json", "JSON string contains a control character");
      this.index += 1;
    }
    throw new SecurityControlError("invalid-json", "JSON string is unterminated");
  }

  private parseNumber(): number {
    const rest = this.text.slice(this.index);
    const match = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(rest);
    if (match === null) throw new SecurityControlError("invalid-json", "JSON number is invalid");
    this.index += match[0].length;
    const value = Number(match[0]);
    if (!Number.isFinite(value)) throw new SecurityControlError("non-finite", "JSON number is not finite");
    return value;
  }

  private literal<T extends JsonValue>(word: string, value: T): T {
    if (this.text.slice(this.index, this.index + word.length) !== word) throw new SecurityControlError("invalid-json", "JSON literal is invalid");
    this.index += word.length;
    return value;
  }

  private skipWhitespace(): void {
    while (this.index < this.text.length && /[\t\n\r ]/.test(this.text[this.index] ?? "")) this.index += 1;
  }
}

export function parseStrictJson(raw: Uint8Array | string, maxBytes = 1_048_576, maxDepth = 32): JsonValue {
  const bytes = typeof raw === "string" ? new TextEncoder().encode(raw) : raw;
  if (bytes.byteLength > maxBytes) throw new SecurityControlError("body-too-large", "JSON body exceeds the configured byte limit", 413);
  let text: string;
  try { text = new TextDecoder("utf-8", { fatal: true }).decode(bytes); }
  catch { throw new SecurityControlError("invalid-utf8", "JSON body is not valid UTF-8"); }
  return new Parser(text, maxDepth).parse();
}
