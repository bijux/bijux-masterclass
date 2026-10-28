import { isAbsolute, relative, resolve, sep } from "node:path";
import { SecurityControlError } from "./errors.js";

const BIDI = /[\u061c\u202a-\u202e\u2066-\u2069]/u;
const CONTROLS = /[\u0000-\u001f\u007f]/u;

export function validateFilename(value: string, maxLength = 160): string {
  if (value.length === 0 || value.length > maxLength || value === "." || value === ".." || value.includes("/") || value.includes("\\") || BIDI.test(value) || CONTROLS.test(value)) throw new SecurityControlError("invalid-filename", "filename is not accepted");
  return value;
}

export function confinedPath(root: string, input: string, percentDecode = true): string {
  let decoded: string;
  try { decoded = percentDecode ? decodeURIComponent(input) : input; }
  catch { throw new SecurityControlError("path-escape", "path encoding is invalid"); }
  if (isAbsolute(decoded)) throw new SecurityControlError("path-escape", "absolute paths are prohibited");
  const base = resolve(root); const candidate = resolve(base, decoded); const rel = relative(base, candidate);
  if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) throw new SecurityControlError("path-escape", "path escapes the configured root");
  return candidate;
}

export interface ArchiveMember { readonly name: string; readonly size: number; readonly kind?: string }
export function validateArchiveMembers(members: readonly ArchiveMember[], options: { maxMembers?: number; maxMemberBytes?: number; maxTotalBytes?: number } = {}): void {
  const maxMembers = options.maxMembers ?? 100; const maxMember = options.maxMemberBytes ?? 10_000_000; const maxTotal = options.maxTotalBytes ?? 50_000_000;
  if (members.length > maxMembers) throw new SecurityControlError("archive-limit", "archive member count exceeds the limit");
  let total = 0;
  for (const member of members) {
    if ((member.kind ?? "file") !== "file") throw new SecurityControlError("archive-entry", "archive contains a prohibited entry type");
    const normalized = member.name.replaceAll("\\", "/");
    if (normalized.startsWith("/") || normalized.split("/").includes("..")) throw new SecurityControlError("archive-path", "archive member path escapes the root");
    validateFilename(normalized.split("/").at(-1) ?? "");
    if (!Number.isSafeInteger(member.size) || member.size < 0 || member.size > maxMember) throw new SecurityControlError("archive-limit", "archive member size exceeds the limit");
    total += member.size; if (total > maxTotal) throw new SecurityControlError("archive-limit", "archive expanded size exceeds the limit");
  }
}
