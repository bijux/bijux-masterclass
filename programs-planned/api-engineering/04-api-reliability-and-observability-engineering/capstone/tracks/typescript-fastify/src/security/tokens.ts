import { createPublicKey, createVerify } from "node:crypto";
import { SecurityControlError } from "./errors.js";
import type { Principal } from "./models.js";
import { parseStrictJson } from "./strict-json.js";

export interface TokenProfile {
  readonly issuer: string;
  readonly audience: string;
  readonly algorithms: readonly string[];
  readonly tokenType: string;
  readonly clockSkewSeconds: number;
  readonly maxLifetimeSeconds: number;
  readonly requiredClaims: readonly string[];
}

export interface JsonWebKey { readonly kid?: string; readonly alg?: string; readonly kty?: string; readonly [key: string]: unknown }
export interface Jwks { readonly keys: readonly JsonWebKey[] }
export interface Revocations { isRevoked(issuer: string, tokenId: string, now: number): boolean }

function decodeSegment(segment: string): Uint8Array {
  try { return Buffer.from(segment, "base64url"); }
  catch { throw new SecurityControlError("invalid-token", "JWT encoding is invalid", 401); }
}

function objectValue(raw: Uint8Array): Record<string, unknown> {
  const value = parseStrictJson(raw);
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new SecurityControlError("invalid-token", "JWT JSON value is not an object", 401);
  return value as Record<string, unknown>;
}

function numeric(claims: Record<string, unknown>, name: string): number {
  const value = claims[name];
  if (typeof value !== "number" || !Number.isSafeInteger(value)) throw new SecurityControlError("invalid-token", `claim ${name} must be an integer NumericDate`, 401);
  return value;
}

function audienceMatches(value: unknown, expected: string): boolean {
  return value === expected || (Array.isArray(value) && value.every((x) => typeof x === "string") && value.includes(expected));
}

export function validateAccessToken(input: {
  token: string; profile: TokenProfile; jwks: Jwks; now: number; revocations: Revocations;
}): Principal {
  const parts = input.token.split(".");
  if (parts.length !== 3 || parts.some((x) => x.length === 0)) throw new SecurityControlError("invalid-token", "credential is not a compact JWT", 401);
  const [encodedHeader, encodedClaims, encodedSignature] = parts as [string, string, string];
  const header = objectValue(decodeSegment(encodedHeader));
  const claims = objectValue(decodeSegment(encodedClaims));
  const alg = header.alg;
  const typ = header.typ;
  const kid = header.kid;
  if (typeof alg !== "string" || !input.profile.algorithms.includes(alg)) throw new SecurityControlError("invalid-token", "JWT algorithm is not accepted", 401);
  if (typ !== input.profile.tokenType) throw new SecurityControlError("invalid-token", "JWT type is not accepted", 401);
  if (typeof kid !== "string" || kid.length === 0) throw new SecurityControlError("invalid-token", "JWT key identifier is required", 401);
  const matches = input.jwks.keys.filter((key) => key.kid === kid);
  if (matches.length !== 1 || matches[0] === undefined) throw new SecurityControlError("invalid-token", "JWT key identifier is unknown or ambiguous", 401);
  const key = createPublicKey({ key: matches[0], format: "jwk" });
  const verifier = createVerify("RSA-SHA256");
  verifier.update(`${encodedHeader}.${encodedClaims}`);
  verifier.end();
  if (!verifier.verify(key, Buffer.from(encodedSignature, "base64url"))) throw new SecurityControlError("invalid-token", "JWT signature is invalid", 401);
  for (const required of input.profile.requiredClaims) if (!(required in claims)) throw new SecurityControlError("invalid-token", `required claim ${required} is missing`, 401);
  if (claims.iss !== input.profile.issuer) throw new SecurityControlError("invalid-token", "JWT issuer is not accepted", 401);
  if (!audienceMatches(claims.aud, input.profile.audience)) throw new SecurityControlError("invalid-token", "JWT audience is not accepted", 401);
  const iat = numeric(claims, "iat"); const exp = numeric(claims, "exp");
  const nbf = claims.nbf === undefined ? iat : numeric(claims, "nbf");
  const skew = input.profile.clockSkewSeconds;
  if (iat > input.now + skew || nbf > input.now + skew) throw new SecurityControlError("invalid-token", "JWT is not yet valid", 401);
  if (exp <= input.now - skew) throw new SecurityControlError("invalid-token", "JWT is expired", 401);
  if (exp <= iat || exp - iat > input.profile.maxLifetimeSeconds) throw new SecurityControlError("invalid-token", "JWT lifetime is not accepted", 401);
  const sub = claims.sub; const tenant = claims.tenant; const jti = claims.jti; const scope = claims.scope;
  if ([sub, tenant, jti, scope].some((x) => typeof x !== "string" || x.length === 0)) throw new SecurityControlError("invalid-token", "JWT identity claims are invalid", 401);
  if (input.revocations.isRevoked(input.profile.issuer, jti as string, input.now)) throw new SecurityControlError("revoked-token", "credential has been revoked", 401);
  const roles = claims.roles ?? [];
  if (!Array.isArray(roles) || !roles.every((x) => typeof x === "string")) throw new SecurityControlError("invalid-token", "roles claim is invalid", 401);
  const authTime = claims.auth_time === undefined ? iat : numeric(claims, "auth_time");
  const assurance = typeof claims.acr === "string" ? claims.acr : "baseline";
  const clientId = typeof claims.client_id === "string" ? claims.client_id : undefined;
  return Object.freeze({ subject: sub as string, tenant: tenant as string, scopes: new Set((scope as string).split(/\s+/).filter(Boolean)), roles: new Set(roles as string[]), ...(clientId ? { clientId } : {}), tokenId: jti as string, assurance, authAgeSeconds: Math.max(0, input.now - authTime) });
}
