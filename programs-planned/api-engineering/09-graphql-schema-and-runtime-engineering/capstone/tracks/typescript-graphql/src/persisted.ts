/** Exact-document persisted-operation registry. */

import { createHash } from "node:crypto";

import { ValidationError } from "./model.js";
import { parseDocument } from "./operation.js";

export interface PersistedOperation {
  sha256: string;
  name: string;
  document: string;
}

export class PersistedOperationRegistry {
  private readonly byHash = new Map<string, PersistedOperation>();
  private readonly byName = new Map<string, PersistedOperation>();

  static digest(document: string): string {
    return createHash("sha256").update(document).digest("hex");
  }

  register(name: string, document: string): PersistedOperation {
    const parsed = parseDocument(document);
    const matches = parsed.operations.filter(
      (operation) => operation.name === name,
    );
    if (matches.length !== 1) {
      throw new ValidationError(
        "persisted operation name mismatch",
      );
    }

    const sha256 = PersistedOperationRegistry.digest(document);
    const existing = this.byName.get(name);
    if (existing && existing.sha256 !== sha256) {
      throw new ValidationError(
        "operation name already registered",
      );
    }

    const value: PersistedOperation = {
      sha256,
      name,
      document,
    };
    this.byHash.set(sha256, value);
    this.byName.set(name, value);
    return value;
  }

  get(hash: string): PersistedOperation {
    const value = this.byHash.get(hash);
    if (!value) {
      throw new ValidationError("unknown persisted operation");
    }
    return value;
  }

  named(name: string): PersistedOperation {
    const value = this.byName.get(name);
    if (!value) {
      throw new ValidationError("unknown operation name");
    }
    return value;
  }
}
