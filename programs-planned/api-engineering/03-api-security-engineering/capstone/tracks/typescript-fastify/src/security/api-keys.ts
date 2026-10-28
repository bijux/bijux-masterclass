import { createHmac, timingSafeEqual } from "node:crypto";
import { SecurityControlError } from "./errors.js";
import type { Principal } from "./models.js";
import { SecretBytes } from "./secrets.js";

export interface ApiKeyRecord { readonly keyId: string; readonly owner: string; readonly tenant: string; readonly digestHex: string; readonly scopes: readonly string[]; readonly revoked?: boolean; readonly expiresAt?: number }

export function digestApiKey(rawKey: string, pepper: SecretBytes): string {
  return createHmac("sha256", pepper.reveal()).update(rawKey, "utf8").digest("hex");
}

export function verifyApiKey(rawKey: string, records: ReadonlyMap<string, ApiKeyRecord>, pepper: SecretBytes, now: number): Principal {
  if (!rawKey.startsWith("ak_") || !rawKey.includes(".")) throw new SecurityControlError("invalid-api-key", "API key format is invalid", 401);
  const keyId = rawKey.slice(3).split(".", 1)[0] ?? "";
  const record = records.get(keyId);
  if (record === undefined) throw new SecurityControlError("invalid-api-key", "API key is invalid", 401);
  const left = Buffer.from(digestApiKey(rawKey, pepper), "hex"); const right = Buffer.from(record.digestHex, "hex");
  if (left.length !== right.length || !timingSafeEqual(left, right)) throw new SecurityControlError("invalid-api-key", "API key is invalid", 401);
  if (record.revoked === true || (record.expiresAt !== undefined && record.expiresAt <= now)) throw new SecurityControlError("invalid-api-key", "API key is inactive", 401);
  return Object.freeze({ subject: record.owner, tenant: record.tenant, scopes: new Set(record.scopes), roles: new Set<string>(), clientId: `api-key:${record.keyId}`, assurance: "baseline", authAgeSeconds: 0 });
}
