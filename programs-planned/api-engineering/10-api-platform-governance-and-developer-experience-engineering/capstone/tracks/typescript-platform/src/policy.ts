export interface Finding {
  ruleId: string; severity: "blocker" | "major" | "minor";
  status: "pass" | "review" | "fail"; entityRef: string; message: string;
}

export function evaluateFindings(findings: Finding[]): "pass" | "review" | "fail" {
  if (findings.some((f) => f.status === "fail" && f.severity === "blocker")) return "fail";
  if (findings.some((f) => f.status === "fail" || f.status === "review")) return "review";
  return "pass";
}

export interface ExceptionGrant {
  id: string; ruleId: string; entityRef: string; owner: string; reason: string;
  compensatingControl: string; approvedBy: string; createdAt: string; expiresAt: string; status: string;
}

export function validateException(record: Partial<ExceptionGrant>, now: Date): [boolean, string] {
  const required: (keyof ExceptionGrant)[] = ["id","ruleId","entityRef","owner","reason","compensatingControl","approvedBy","createdAt","expiresAt","status"];
  const missing = required.filter((key) => !record[key]);
  if (missing.length) return [false, `missing:${missing.join(",")}`];
  if (record.status !== "active") return [false, "exception-not-active"];
  if (new Date(record.expiresAt!).getTime() <= now.getTime()) return [false, "exception-expired"];
  return [true, "valid"];
}
