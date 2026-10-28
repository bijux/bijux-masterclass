import { SecurityControlError } from "./errors.js";

const CRITICAL = new Set(["authorization", "content-length", "host", "x-api-key", "x-forwarded-host", "x-forwarded-proto"]);

export interface EdgeContext {
  readonly clientPeer: string;
  readonly externalScheme: string;
  readonly externalHost: string;
  readonly origin: string;
  readonly trustedProxy: boolean;
}

function headerMap(headers: readonly (readonly [string, string])[]): Map<string, string[]> {
  const result = new Map<string, string[]>();
  for (const [name, value] of headers) {
    const key = name.trim().toLowerCase();
    result.set(key, [...(result.get(key) ?? []), value.trim()]);
  }
  for (const name of CRITICAL) {
    if ((result.get(name)?.length ?? 0) > 1) throw new SecurityControlError("ambiguous-header", `multiple ${name} header fields`);
  }
  return result;
}

function trusted(peer: string, configured: readonly string[]): boolean {
  // The dependency-light reference accepts exact addresses. CIDR handling belongs
  // to the environment-backed adapter and is not silently simulated here.
  return configured.includes(peer);
}

export function evaluateEdge(input: {
  peer: string;
  headers: readonly (readonly [string, string])[];
  allowedHosts: readonly string[];
  trustedProxies?: readonly string[];
  directScheme?: string;
}): EdgeContext {
  const headers = headerMap(input.headers);
  const isTrusted = trusted(input.peer, input.trustedProxies ?? []);
  let host = (headers.get("host")?.[0] ?? "").toLowerCase();
  let scheme = (input.directScheme ?? "https").toLowerCase();
  if (isTrusted) {
    host = (headers.get("x-forwarded-host")?.[0] ?? host).toLowerCase();
    scheme = (headers.get("x-forwarded-proto")?.[0] ?? scheme).toLowerCase();
  }
  if (scheme !== "https" && scheme !== "http") throw new SecurityControlError("scheme-not-allowed", "external scheme is not accepted");
  if (!input.allowedHosts.map((x) => x.toLowerCase()).includes(host)) throw new SecurityControlError("host-not-allowed", "external host is not accepted");
  return Object.freeze({ clientPeer: input.peer, externalScheme: scheme, externalHost: host, origin: `${scheme}://${host}`, trustedProxy: isTrusted });
}
