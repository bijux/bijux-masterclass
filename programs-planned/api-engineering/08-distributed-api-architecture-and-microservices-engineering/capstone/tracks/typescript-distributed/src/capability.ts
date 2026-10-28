import { createHmac, timingSafeEqual } from "node:crypto";

import { Unauthorized, ValidationError } from "./model.js";

export interface CapabilityClaims {
  jti: string;
  issuer: string;
  audience: string;
  subject: string;
  tenant: string;
  resource: string;
  action: string;
  issuedAt: number;
  expiresAt: number;
  sha256?: string;
  maxBytes?: number;
}

interface WireClaims {
  action: string;
  audience: string;
  expires_at: number;
  issued_at: number;
  issuer: string;
  jti: string;
  max_bytes?: number;
  resource: string;
  sha256?: string;
  subject: string;
  tenant: string;
}

function toWire(claims: CapabilityClaims): WireClaims {
  const wire: WireClaims = {
    action: claims.action,
    audience: claims.audience,
    expires_at: claims.expiresAt,
    issued_at: claims.issuedAt,
    issuer: claims.issuer,
    jti: claims.jti,
    resource: claims.resource,
    subject: claims.subject,
    tenant: claims.tenant,
  };
  if (claims.maxBytes !== undefined) wire.max_bytes = claims.maxBytes;
  if (claims.sha256 !== undefined) wire.sha256 = claims.sha256;
  return wire;
}

function fromWire(raw: unknown): CapabilityClaims {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) {
    throw new Unauthorized("capability payload must be an object");
  }
  const value = raw as Record<string, unknown>;
  const required = [
    "action",
    "audience",
    "expires_at",
    "issued_at",
    "issuer",
    "jti",
    "resource",
    "subject",
    "tenant",
  ] as const;
  const allowed = new Set([...required, "max_bytes", "sha256"]);
  if (required.some((key) => !(key in value))) {
    throw new Unauthorized("capability payload fields are invalid");
  }
  if (Object.keys(value).some((key) => !allowed.has(key))) {
    throw new Unauthorized("capability payload fields are invalid");
  }
  const integer = (key: "issued_at" | "expires_at" | "max_bytes"): number => {
    const candidate = value[key];
    if (!Number.isSafeInteger(candidate)) {
      throw new Unauthorized(`capability ${key} must be a safe integer`);
    }
    return candidate as number;
  };
  const string = (key: string): string => {
    const candidate = value[key];
    if (typeof candidate !== "string" || candidate.length === 0) {
      throw new Unauthorized(`capability ${key} must be a non-empty string`);
    }
    return candidate;
  };
  const claims: CapabilityClaims = {
    action: string("action"),
    audience: string("audience"),
    expiresAt: integer("expires_at"),
    issuedAt: integer("issued_at"),
    issuer: string("issuer"),
    jti: string("jti"),
    resource: string("resource"),
    subject: string("subject"),
    tenant: string("tenant"),
  };
  if (value.max_bytes !== undefined) claims.maxBytes = integer("max_bytes");
  if (value.sha256 !== undefined) claims.sha256 = string("sha256");
  return claims;
}

function canonical(value: WireClaims): string {
  const ordered: Record<string, unknown> = {};
  for (const key of Object.keys(value).sort()) {
    ordered[key] = value[key as keyof WireClaims];
  }
  return JSON.stringify(ordered);
}

function base64UrlEncode(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/u, "");
}

function base64UrlDecode(value: string): Uint8Array {
  if (!/^[A-Za-z0-9_-]*$/u.test(value)) {
    throw new Unauthorized("malformed capability encoding");
  }
  const padded = value.replace(/-/g, "+").replace(/_/g, "/") +
    "=".repeat((4 - (value.length % 4)) % 4);
  try {
    const binary = atob(padded);
    return Uint8Array.from(binary, (character) => character.charCodeAt(0));
  } catch (error) {
    throw new Unauthorized("malformed capability encoding", { cause: error });
  }
}

function hexToBytes(value: string): Uint8Array {
  if (value.length % 2 !== 0 || !/^[0-9a-f]+$/u.test(value)) {
    throw new Unauthorized("invalid capability signature encoding");
  }
  const bytes = new Uint8Array(value.length / 2);
  for (let index = 0; index < bytes.length; index += 1) {
    bytes[index] = Number.parseInt(value.slice(index * 2, index * 2 + 2), 16);
  }
  return bytes;
}

export class CapabilityAuthority {
  private readonly consumed = new Set<string>();

  constructor(
    readonly issuer: string,
    private readonly key: string,
  ) {
    if (new TextEncoder().encode(key).length < 16) {
      throw new ValidationError("capability key is too short");
    }
  }

  mint(claims: CapabilityClaims): string {
    if (claims.issuer !== this.issuer) {
      throw new ValidationError("issuer mismatch");
    }
    if (claims.expiresAt <= claims.issuedAt) {
      throw new ValidationError("invalid capability lifetime");
    }
    if (claims.maxBytes !== undefined && claims.maxBytes <= 0) {
      throw new ValidationError("maxBytes must be positive");
    }
    const payload = base64UrlEncode(
      new TextEncoder().encode(canonical(toWire(claims))),
    );
    const signature = base64UrlEncode(
      hexToBytes(createHmac("sha256", this.key).update(payload).digest("hex")),
    );
    return `cap1.${payload}.${signature}`;
  }

  verify(
    token: string,
    expected: {
      audience: string;
      tenant: string;
      action: string;
      now: number;
      consumeOnce?: boolean;
    },
  ): CapabilityClaims {
    const parts = token.split(".");
    if (parts.length !== 3 || parts[0] !== "cap1") {
      throw new Unauthorized("malformed capability");
    }
    const payload = parts[1]!;
    const signature = base64UrlDecode(parts[2]!);
    const expectedSignature = hexToBytes(
      createHmac("sha256", this.key).update(payload).digest("hex"),
    );
    if (
      signature.length !== expectedSignature.length ||
      !timingSafeEqual(signature, expectedSignature)
    ) {
      throw new Unauthorized("invalid capability signature");
    }
    let raw: unknown;
    try {
      raw = JSON.parse(new TextDecoder().decode(base64UrlDecode(payload)));
    } catch (error) {
      if (error instanceof Unauthorized) throw error;
      throw new Unauthorized("malformed capability payload", { cause: error });
    }
    const claims = fromWire(raw);
    if (claims.issuer !== this.issuer || claims.audience !== expected.audience) {
      throw new Unauthorized("capability audience or issuer mismatch");
    }
    if (claims.tenant !== expected.tenant || claims.action !== expected.action) {
      throw new Unauthorized("capability authority mismatch");
    }
    if (expected.now < claims.issuedAt || expected.now >= claims.expiresAt) {
      throw new Unauthorized("capability expired or not active");
    }
    if (expected.consumeOnce) {
      if (this.consumed.has(claims.jti)) {
        throw new Unauthorized("capability already consumed");
      }
      this.consumed.add(claims.jti);
    }
    return claims;
  }
}
