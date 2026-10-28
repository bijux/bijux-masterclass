import { ValidationError } from "./model.js";
const allowed = new Set(["Project", "AnalysisRun", "Artifact"]);
export function encodeGlobalId(typeName: string, localId: string): string {
  if (!allowed.has(typeName) || !localId) throw new ValidationError("unsupported global identifier");
  return Buffer.from(`${typeName}:${localId}`, "utf8").toString("base64url");
}
export function decodeGlobalId(value: string): readonly [string, string] {
  try {
    const raw = Buffer.from(value, "base64url").toString("utf8");
    const index = raw.indexOf(":"); if (index <= 0) throw new Error("separator");
    const typeName = raw.slice(0,index), localId = raw.slice(index+1);
    if (!allowed.has(typeName) || !localId) throw new Error("unsupported");
    return [typeName,localId] as const;
  } catch { throw new ValidationError("malformed global identifier") }
}
