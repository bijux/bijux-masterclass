/**
 * A bounded GraphQL document parser used by dependency-light course proofs.
 *
 * It covers the operation and selection shapes in the released operation
 * registry. It is intentionally not represented as a standards-complete
 * parser; the optional framework proof uses a production GraphQL runtime.
 */

import { ValidationError } from "./model.js";

export type Selection =
  | FieldNode
  | FragmentSpread
  | InlineFragment;

export interface FieldNode {
  kind: "field";
  name: string;
  alias?: string;
  selections: readonly Selection[];
  arguments: readonly string[];
}

export interface FragmentSpread {
  kind: "spread";
  name: string;
}

export interface InlineFragment {
  kind: "inline";
  typeCondition?: string;
  selections: readonly Selection[];
}

export interface FragmentDefinition {
  name: string;
  typeCondition: string;
  selections: readonly Selection[];
}

export interface OperationDefinition {
  operationType: "query" | "mutation" | "subscription";
  name?: string;
  selections: readonly Selection[];
}

export interface Document {
  operations: readonly OperationDefinition[];
  fragments: ReadonlyMap<string, FragmentDefinition>;
}

const punctuators = new Set("!$&():=@[]{|}".split(""));

export function tokenize(source: string): string[] {
  const tokens: string[] = [];
  let index = 0;

  while (index < source.length) {
    const character = source[index]!;

    if (" \t\r\n,".includes(character)) {
      index += 1;
      continue;
    }

    if (character === "#") {
      while (
        index < source.length &&
        !"\r\n".includes(source[index]!)
      ) {
        index += 1;
      }
      continue;
    }

    if (source.startsWith("...", index)) {
      tokens.push("...");
      index += 3;
      continue;
    }

    if (punctuators.has(character)) {
      tokens.push(character);
      index += 1;
      continue;
    }

    if (character === '"') {
      const start = index;
      index += 1;
      let escaped = false;
      let terminated = false;

      while (index < source.length) {
        const current = source[index]!;
        if (escaped) {
          escaped = false;
        } else if (current === "\\") {
          escaped = true;
        } else if (current === '"') {
          index += 1;
          terminated = true;
          break;
        }
        index += 1;
      }

      if (!terminated) {
        throw new ValidationError("unterminated string");
      }
      tokens.push(source.slice(start, index));
      continue;
    }

    if (/[A-Za-z_]/.test(character)) {
      const start = index;
      index += 1;
      while (
        index < source.length &&
        /[A-Za-z0-9_]/.test(source[index]!)
      ) {
        index += 1;
      }
      tokens.push(source.slice(start, index));
      continue;
    }

    if (/[0-9-]/.test(character)) {
      const start = index;
      index += 1;
      while (
        index < source.length &&
        /[0-9.eE+\-]/.test(source[index]!)
      ) {
        index += 1;
      }
      tokens.push(source.slice(start, index));
      continue;
    }

    throw new ValidationError(
      `unexpected GraphQL token at character ${index}`,
    );
  }

  return tokens;
}

class Parser {
  private index = 0;

  constructor(private readonly tokens: readonly string[]) {}

  private peek(value?: string): boolean {
    if (this.index >= this.tokens.length) {
      return false;
    }
    return (
      value === undefined || this.tokens[this.index] === value
    );
  }

  private take(value?: string): string {
    if (this.index >= this.tokens.length) {
      throw new ValidationError("unexpected end of document");
    }

    const token = this.tokens[this.index]!;
    if (value !== undefined && token !== value) {
      throw new ValidationError(
        `expected ${JSON.stringify(value)}, ` +
          `got ${JSON.stringify(token)}`,
      );
    }
    this.index += 1;
    return token;
  }

  private skipBalanced(opening: string, closing: string): void {
    this.take(opening);
    let depth = 1;
    while (depth > 0) {
      const token = this.take();
      if (token === opening) {
        depth += 1;
      } else if (token === closing) {
        depth -= 1;
      }
    }
  }

  private skipDirectives(): void {
    while (this.peek("@")) {
      this.take("@");
      this.take();
      if (this.peek("(")) {
        this.skipBalanced("(", ")");
      }
    }
  }

  private selectionSet(): readonly Selection[] {
    this.take("{");
    const selections: Selection[] = [];

    while (!this.peek("}")) {
      if (this.peek("...")) {
        this.take("...");
        if (this.peek("on")) {
          this.take("on");
          const typeCondition = this.take();
          this.skipDirectives();
          selections.push({
            kind: "inline",
            typeCondition,
            selections: this.selectionSet(),
          });
        } else {
          const name = this.take();
          this.skipDirectives();
          selections.push({ kind: "spread", name });
        }
        continue;
      }

      const first = this.take();
      let alias: string | undefined;
      let name = first;

      if (this.peek(":")) {
        this.take(":");
        alias = first;
        name = this.take();
      }

      const arguments_: string[] = [];
      if (this.peek("(")) {
        const start = this.index;
        this.skipBalanced("(", ")");
        arguments_.push(...this.tokens.slice(start, this.index));
      }

      this.skipDirectives();
      const nested = this.peek("{") ? this.selectionSet() : [];
      selections.push({
        kind: "field",
        name,
        alias,
        selections: nested,
        arguments: arguments_,
      });
    }

    this.take("}");
    return selections;
  }

  parse(): Document {
    const operations: OperationDefinition[] = [];
    const fragments = new Map<string, FragmentDefinition>();

    while (this.peek()) {
      if (this.peek("fragment")) {
        this.take("fragment");
        const name = this.take();
        this.take("on");
        const typeCondition = this.take();
        this.skipDirectives();

        if (fragments.has(name)) {
          throw new ValidationError("duplicate fragment");
        }
        fragments.set(name, {
          name,
          typeCondition,
          selections: this.selectionSet(),
        });
        continue;
      }

      if (this.peek("{")) {
        operations.push({
          operationType: "query",
          selections: this.selectionSet(),
        });
        continue;
      }

      const rawType = this.take();
      if (
        rawType !== "query" &&
        rawType !== "mutation" &&
        rawType !== "subscription"
      ) {
        throw new ValidationError("unknown operation type");
      }

      const name =
        this.peek("{") || this.peek("(") || this.peek("@")
          ? undefined
          : this.take();

      if (this.peek("(")) {
        this.skipBalanced("(", ")");
      }
      this.skipDirectives();

      operations.push({
        operationType: rawType,
        name,
        selections: this.selectionSet(),
      });
    }

    if (operations.length === 0) {
      throw new ValidationError("document contains no operation");
    }

    return { operations, fragments };
  }
}

export function parseDocument(source: string): Document {
  return new Parser(tokenize(source)).parse();
}
