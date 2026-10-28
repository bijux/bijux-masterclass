import { entityRef, parseRef } from "./identifiers.js";

export interface EntityRecord {
  kind: string; namespace?: string; name: string; title?: string;
  owner?: string | null; lifecycle?: string; system?: string | null;
  providesApis?: string[]; consumesApis?: string[]; dependsOn?: string[];
  [key: string]: unknown;
}

const ownerKinds = new Set(["component", "api", "resource", "system", "domain"]);
const lifecycles = new Set(["proposed", "experimental", "active", "deprecated", "retired"]);

export class Catalog {
  readonly entities = new Map<string, EntityRecord>();

  constructor(records: EntityRecord[]) {
    for (const record of records) {
      const ref = entityRef(record.kind, record.namespace ?? "default", record.name);
      if (this.entities.has(ref)) throw new Error(`duplicate-entity:${ref}`);
      this.entities.set(ref, { ...record, kind: record.kind.toLowerCase(), namespace: record.namespace ?? "default", lifecycle: record.lifecycle ?? "active" });
    }
    this.validate();
  }

  validate(): void {
    const implemented = new Map<string, number>();
    for (const [ref, entity] of this.entities) if (entity.kind === "api") implemented.set(ref, 0);
    for (const [ref, entity] of this.entities) {
      if (!lifecycles.has(String(entity.lifecycle))) throw new Error(`invalid-lifecycle:${ref}`);
      if (ownerKinds.has(entity.kind)) {
        if (!entity.owner) throw new Error(`missing-owner:${ref}`);
        parseRef(entity.owner);
        const owner = this.entities.get(entity.owner);
        if (!owner) throw new Error(`unknown-owner:${ref}:${entity.owner}`);
        if (owner.kind !== "group") throw new Error(`owner-not-group:${ref}`);
      }
      if (["component", "api", "resource"].includes(entity.kind)) {
        if (!entity.system) throw new Error(`missing-system:${ref}`);
        const system = this.entities.get(entity.system);
        if (!system || system.kind !== "system") throw new Error(`invalid-system:${ref}`);
      }
      for (const target of [...(entity.providesApis ?? []), ...(entity.consumesApis ?? []), ...(entity.dependsOn ?? [])]) {
        parseRef(target);
        if (!this.entities.has(target)) throw new Error(`unknown-relation:${ref}:${target}`);
      }
      if (entity.kind === "component") {
        for (const apiRef of entity.providesApis ?? []) {
          if (this.entities.get(apiRef)?.kind !== "api") throw new Error(`provides-non-api:${apiRef}`);
          implemented.set(apiRef, (implemented.get(apiRef) ?? 0) + 1);
        }
      }
    }
    for (const [apiRef, count] of implemented) if (count === 0) throw new Error(`orphan-api:${apiRef}`);
  }

  ownerOf(ref: string): string {
    const entity = this.entities.get(ref);
    if (!entity) throw new Error(`unknown-entity:${ref}`);
    if (!entity.owner) throw new Error(`entity-has-no-owner:${ref}`);
    return entity.owner;
  }

  consumersOf(apiRef: string): string[] {
    return [...this.entities].filter(([, entity]) => (entity.consumesApis ?? []).includes(apiRef)).map(([ref]) => ref).sort();
  }
}
