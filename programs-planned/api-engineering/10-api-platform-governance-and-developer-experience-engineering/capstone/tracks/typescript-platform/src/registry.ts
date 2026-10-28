import { createHash } from "node:crypto";

export interface ReleaseRecord {
  apiRef: string; protocol: string; version: string; source: string; sha256: string;
  lifecycle: string; owner: string; compatibilityEvidence: string; publishedAt: string;
}

export function sha256(data: Uint8Array): string {
  return createHash("sha256").update(data).digest("hex");
}

export class ContractRegistry {
  readonly releases = new Map<string, ReleaseRecord>();

  constructor(records: ReleaseRecord[] = []) {
    for (const record of records) {
      if (!/^[0-9a-f]{64}$/.test(record.sha256)) throw new Error("invalid-digest");
      const key = `${record.apiRef}@${record.version}`;
      if (this.releases.has(key)) throw new Error("duplicate-release-record");
      this.releases.set(key, { ...record });
    }
  }

  publish(record: Omit<ReleaseRecord, "sha256">, data: Uint8Array): "published" | "idempotent" {
    if (!record.compatibilityEvidence) throw new Error("missing-compatibility-evidence");
    const digest = sha256(data);
    const key = `${record.apiRef}@${record.version}`;
    const existing = this.releases.get(key);
    if (existing) {
      if (existing.sha256 !== digest) throw new Error("immutable-release");
      return "idempotent";
    }
    this.releases.set(key, { ...record, sha256: digest });
    return "published";
  }
}
