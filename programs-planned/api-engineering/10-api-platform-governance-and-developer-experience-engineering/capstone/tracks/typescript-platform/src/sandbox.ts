import { createHash } from "node:crypto";

export interface SandboxProfile {
  dataClass: string; productionDataAllowed: boolean; tenantPrefix: string;
  sessionTtlSeconds: number; credentialTtlSeconds: number;
}
export interface SandboxSession { id: string; tenant: string; createdAt: Date; expiresAt: Date; credentialExpiresAt: Date; dataClass: string; }

export function createSession(subject: string, nonce: string, now: Date, profile: SandboxProfile): SandboxSession {
  if (profile.dataClass !== "synthetic-only" || profile.productionDataAllowed !== false) throw new Error("unsafe-sandbox-profile");
  const digest = createHash("sha256").update(`${subject}\0${nonce}`).digest("hex").slice(0,16);
  return { id:`sbx-${digest}`, tenant:`${profile.tenantPrefix}${digest.slice(0,10)}`, createdAt:now,
    expiresAt:new Date(now.getTime()+profile.sessionTtlSeconds*1000), credentialExpiresAt:new Date(now.getTime()+profile.credentialTtlSeconds*1000), dataClass:"synthetic-only" };
}

export function validateImport(dataClass: string): void {
  if (dataClass !== "synthetic-only") throw new Error("production-data-forbidden");
}
