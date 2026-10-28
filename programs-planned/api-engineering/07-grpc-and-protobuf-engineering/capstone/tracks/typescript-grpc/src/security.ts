import { timingSafeEqual } from "node:crypto";
import type { Principal } from "./model.js";

const fixtures: Readonly<Record<string, Principal>> = {
  "learner-read": {
    subject: "user-read", tenant: "tenant-a",
    scopes: new Set(["runs:read"]), workload: "gateway",
  },
  "learner-write": {
    subject: "user-write", tenant: "tenant-a",
    scopes: new Set(["runs:read", "runs:write", "datasets:write", "artifacts:read"]),
    workload: "gateway",
  },
  "tenant-b-write": {
    subject: "user-b", tenant: "tenant-b",
    scopes: new Set(["runs:read", "runs:write", "datasets:write", "artifacts:read"]),
    workload: "gateway",
  },
  "worker-1": {
    subject: "worker-1", tenant: "tenant-a",
    scopes: new Set(["worker:connect"]), workload: "worker",
  },
};

export function authenticate(values: readonly string[]): Principal {
  if (values.length !== 1) throw new Error("UNAUTHENTICATED");
  const value = values[0];
  if (value === undefined || !value.startsWith("Bearer ")) {
    throw new Error("UNAUTHENTICATED");
  }
  const principal = fixtures[value.slice(7)];
  if (principal === undefined) throw new Error("UNAUTHENTICATED");
  return principal;
}

export function requireScope(principal: Principal, scope: string): void {
  if (!principal.scopes.has(scope)) throw new Error("PERMISSION_DENIED");
}

export function tenantOf(resource: string): string {
  return resource.startsWith("projects/p-b-") ? "tenant-b" : "tenant-a";
}

export function requireTenant(principal: Principal, resource: string): void {
  if (principal.tenant !== tenantOf(resource.split("/runs/")[0] ?? resource)) {
    throw new Error("PERMISSION_DENIED");
  }
}

export function constantTimeEqual(left: Uint8Array, right: Uint8Array): boolean {
  return left.byteLength === right.byteLength &&
    timingSafeEqual(Buffer.from(left), Buffer.from(right));
}
