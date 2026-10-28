import { ValidationError } from "./model.js";

interface Entry<Value> {
  version: number;
  value: Value;
  updatedAtMs: number;
}

export type ProjectionOutcome = "apply" | "duplicate" | "stale" | "gap";

export class VersionedProjection<Value> {
  private readonly items = new Map<string, Entry<Value>>();
  private readonly gapMap = new Map<string, readonly [number, number]>();

  apply(
    key: string,
    version: number,
    value: Value,
    nowMs: number,
  ): ProjectionOutcome {
    if (!Number.isSafeInteger(version) || version <= 0) {
      throw new ValidationError("version must be a positive safe integer");
    }
    const current = this.items.get(key);
    if (!current) {
      if (version !== 1) {
        this.gapMap.set(key, [0, version]);
        return "gap";
      }
      this.items.set(key, { version, value, updatedAtMs: nowMs });
      return "apply";
    }
    if (version === current.version) return "duplicate";
    if (version < current.version) return "stale";
    if (version > current.version + 1) {
      this.gapMap.set(key, [current.version, version]);
      return "gap";
    }
    this.items.set(key, { version, value, updatedAtMs: nowMs });
    this.gapMap.delete(key);
    return "apply";
  }

  get(key: string, nowMs: number, maxStalenessMs: number): Value {
    if (this.gapMap.has(key)) {
      throw new ValidationError(`projection has unresolved gap: ${key}`);
    }
    const entry = this.items.get(key);
    if (!entry) throw new ValidationError(`missing projection: ${key}`);
    if (nowMs - entry.updatedAtMs > maxStalenessMs) {
      throw new ValidationError(`projection stale: ${key}`);
    }
    return entry.value;
  }

  version(key: string): number {
    const entry = this.items.get(key);
    if (!entry) throw new ValidationError(`missing projection: ${key}`);
    return entry.version;
  }

  gaps(): ReadonlyMap<string, readonly [number, number]> {
    return this.gapMap;
  }
}
