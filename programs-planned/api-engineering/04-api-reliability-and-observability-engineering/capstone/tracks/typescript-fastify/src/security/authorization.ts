import type { Decision, Principal, ResourceFacts } from "./models.js";

export interface Policy { readonly operationId: string; readonly scopes: ReadonlySet<string>; readonly roles: ReadonlySet<string>; readonly relationship: string; readonly tenantBound: boolean; readonly conceal: boolean; readonly requiredAssurance: string; readonly maxAuthAgeSeconds?: number }

function relationshipAllowed(name: string, principal: Principal, resource: ResourceFacts): boolean {
  if (["none", "tenant-query", "tenant-create"].includes(name)) return true;
  if (name === "owner") return resource.owner === principal.subject;
  if (["owner-or-member", "project-member", "project-member-and-dataset", "project-member-completed-run"].includes(name)) return resource.owner === principal.subject || resource.members.has(principal.subject);
  if (["project-owner-or-writer", "project-owner", "tenant-owner"].includes(name)) return resource.owner === principal.subject || principal.roles.has("tenant-admin");
  if (name === "project-owner-or-run-creator") return resource.owner === principal.subject || resource.creator === principal.subject || principal.roles.has("tenant-admin");
  if (name === "fresh-high-assurance") return principal.roles.has("operator");
  return false;
}

export function authorize(operationId: string, principal: Principal | undefined, resource: ResourceFacts, policies: ReadonlyMap<string, Policy>): Decision {
  const policy = policies.get(operationId);
  if (policy === undefined) return { allowed: false, reason: "policy.missing", conceal: false, obligations: [] };
  if (operationId === "getHealth" && principal === undefined) return { allowed: true, reason: "policy.public", conceal: false, obligations: [] };
  if (principal === undefined) return { allowed: false, reason: "credential.required", conceal: policy.conceal, obligations: [] };
  if (![...policy.scopes].every((scope) => principal.scopes.has(scope))) return { allowed: false, reason: "scope.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.roles.size > 0 && ![...policy.roles].some((role) => principal.roles.has(role))) return { allowed: false, reason: "role.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.tenantBound && resource.tenant !== undefined && resource.tenant !== principal.tenant) return { allowed: false, reason: "tenant.foreign", conceal: policy.conceal, obligations: [] };
  if (!relationshipAllowed(policy.relationship, principal, resource)) return { allowed: false, reason: "relationship.denied", conceal: policy.conceal, obligations: [] };
  if (policy.requiredAssurance === "high" && principal.assurance !== "high") return { allowed: false, reason: "assurance.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.maxAuthAgeSeconds !== undefined && principal.authAgeSeconds > policy.maxAuthAgeSeconds) return { allowed: false, reason: "authentication.stale", conceal: policy.conceal, obligations: ["step-up"] };
  return { allowed: true, reason: "policy.allow", conceal: false, obligations: ["audit"] };
}
