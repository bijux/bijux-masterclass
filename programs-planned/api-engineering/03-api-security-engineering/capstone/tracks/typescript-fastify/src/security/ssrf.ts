import { SecurityControlError } from "./errors.js";

export interface ValidatedDestination { readonly url: string; readonly hostname: string; readonly port: number; readonly addresses: readonly string[] }

function publicIpv4(value: string): boolean {
  const parts = value.split(".").map(Number); if (parts.length !== 4 || parts.some((x) => !Number.isInteger(x) || x < 0 || x > 255)) return false;
  const [a,b] = parts as [number,number,number,number];
  if (a === 0 || a === 10 || a === 127 || a >= 224) return false;
  if (a === 100 && b >= 64 && b <= 127) return false;
  if (a === 169 && b === 254) return false;
  if (a === 172 && b >= 16 && b <= 31) return false;
  if (a === 192 && (b === 0 || b === 168)) return false;
  if (a === 198 && (b === 18 || b === 19 || b === 51)) return false;
  if (a === 203 && b === 0) return false;
  return true;
}

function publicAddress(value: string): boolean {
  const lower = value.toLowerCase();
  if (lower.startsWith("::ffff:")) return publicIpv4(lower.slice(7));
  if (value.includes(".")) return publicIpv4(value);
  if (lower === "::" || lower === "::1" || lower.startsWith("fe80:") || lower.startsWith("fc") || lower.startsWith("fd") || lower.startsWith("2001:db8:")) return false;
  return /^[0-9a-f:]+$/u.test(lower) && /^[23]/u.test(lower);
}

export function validateDestination(input: { url: string; addresses: readonly string[]; allowedSchemes?: readonly string[]; allowedPorts?: readonly number[] }): ValidatedDestination {
  let parsed: URL; try { parsed = new URL(input.url); } catch { throw new SecurityControlError("invalid-url", "outbound URL is invalid"); }
  const schemes = input.allowedSchemes ?? ["https:"]; if (!schemes.map((x) => x.endsWith(":") ? x : `${x}:`).includes(parsed.protocol)) throw new SecurityControlError("scheme", "outbound URL scheme is prohibited");
  if (parsed.username !== "" || parsed.password !== "") throw new SecurityControlError("userinfo", "outbound URL user information is prohibited");
  if (parsed.hash !== "") throw new SecurityControlError("fragment", "outbound URL fragment is prohibited");
  const port = parsed.port === "" ? (parsed.protocol === "https:" ? 443 : 80) : Number(parsed.port);
  if (!(input.allowedPorts ?? [443]).includes(port)) throw new SecurityControlError("port", "outbound URL port is prohibited");
  if (input.addresses.length === 0) throw new SecurityControlError("dns-empty", "outbound host resolved to no addresses");
  if (!input.addresses.every(publicAddress)) throw new SecurityControlError("forbidden-address", "outbound host resolves to a forbidden address");
  return Object.freeze({ url: input.url, hostname: parsed.hostname.toLowerCase(), port, addresses: [...input.addresses] });
}

export function verifyConnectedPeer(destination: ValidatedDestination, peer: string): void {
  if (!destination.addresses.includes(peer)) throw new SecurityControlError("peer-mismatch", "connected peer was not approved for this request");
}
