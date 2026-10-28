export interface CompatibilityIssue { readonly severity: "breaking" | "review" | "additive"; readonly path: string; readonly message: string }
export interface CompatibilityReport { readonly status: "accepted" | "review-required" | "rejected"; readonly issues: readonly CompatibilityIssue[] }

type Schema = Record<string, any>;

function types(schema: Schema): string[] {
  const value = schema.type;
  if (typeof value === "string") return [value];
  if (Array.isArray(value)) return value.map(String);
  return [];
}

export function compareObjectSchemas(oldSchema: Schema, newSchema: Schema): CompatibilityReport {
  const issues: CompatibilityIssue[] = [];
  const oldRequired = new Set<string>(oldSchema.required ?? []);
  const newRequired = new Set<string>(newSchema.required ?? []);
  for (const name of [...newRequired].sort()) if (!oldRequired.has(name)) issues.push({ severity: "breaking", path: `$.${name}`, message: "field became newly required" });
  const before: Record<string, Schema> = oldSchema.properties ?? {};
  const after: Record<string, Schema> = newSchema.properties ?? {};
  for (const name of Object.keys(before).sort()) if (!(name in after)) issues.push({ severity: "breaking", path: `$.${name}`, message: "previously available field was removed" });
  for (const name of Object.keys(before).filter((key) => key in after).sort()) {
    const left = before[name] ?? {};
    const right = after[name] ?? {};
    if (JSON.stringify(types(left)) !== JSON.stringify(types(right))) issues.push({ severity: "breaking", path: `$.${name}`, message: "field type changed" });
    const oldEnum = new Set(left.enum ?? []);
    const newEnum = new Set(right.enum ?? []);
    if (oldEnum.size && [...oldEnum].some((value) => !newEnum.has(value))) issues.push({ severity: "breaking", path: `$.${name}`, message: "enum was narrowed" });
    else if (oldEnum.size && [...newEnum].some((value) => !oldEnum.has(value))) issues.push({ severity: "review", path: `$.${name}`, message: "enum gained values; strict consumers may fail" });
  }
  for (const name of Object.keys(after).sort()) if (!(name in before) && !newRequired.has(name)) issues.push({ severity: "additive", path: `$.${name}`, message: "optional field added" });
  const status = issues.some((item) => item.severity === "breaking") ? "rejected" : issues.some((item) => item.severity === "review") ? "review-required" : "accepted";
  return { status, issues };
}
