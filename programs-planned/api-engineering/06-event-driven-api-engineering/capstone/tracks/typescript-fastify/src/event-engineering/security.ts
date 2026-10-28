import { createHmac, timingSafeEqual } from "node:crypto";
import { envelopeBytes, type EventEnvelope } from "./envelope.js";

const SENSITIVE = new Set(["accesstoken", "refreshtoken", "password", "rawdataset", "webhooksecret", "authorization", "leasetoken", "stacktrace"]);

export class SecurityError extends Error {}
export interface ProducerGrant { producerId: string; sources: ReadonlySet<string>; channels: ReadonlySet<string>; eventTypes: ReadonlySet<string>; tenants: ReadonlySet<string> }
export interface SignedMessage { keyId: string; timestamp: string; signature: string; body: Uint8Array }

function sensitivePaths(value: unknown, path = "$"): string[] {
  const found: string[] = [];
  if (Array.isArray(value)) value.forEach((item, index) => found.push(...sensitivePaths(item, `${path}[${index}]`)));
  else if (value !== null && typeof value === "object") {
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
      const normalized = key.toLowerCase().replace(/[^a-z0-9]/g, "");
      if (SENSITIVE.has(normalized)) found.push(`${path}.${key}`);
      found.push(...sensitivePaths(item, `${path}.${key}`));
    }
  }
  return found;
}

export function authorizeMessage(grant: ProducerGrant, channel: string, event: EventEnvelope): void {
  if (!grant.sources.has(event.source)) throw new SecurityError("source not granted");
  if (!grant.channels.has(channel)) throw new SecurityError("channel not granted");
  if (!grant.eventTypes.has(event.type)) throw new SecurityError("event type not granted");
  if (!grant.tenants.has(event.tenantid)) throw new SecurityError("tenant not granted");
  const sensitive = sensitivePaths(event.data);
  if (sensitive.length) throw new SecurityError(`sensitive fields prohibited: ${sensitive.join(",")}`);
}

export function signMessage(event: EventEnvelope, keyId: string, secret: Uint8Array, timestamp: Date): SignedMessage {
  const text = timestamp.toISOString().replace(".000Z", "Z");
  const body = envelopeBytes(event);
  const mac = createHmac("sha256", secret).update(`${text}\n`).update(body).digest("hex");
  return { keyId, timestamp: text, signature: `sha256=${mac}`, body };
}

export function verifyMessage(message: SignedMessage, keys: ReadonlyMap<string, Uint8Array>, now: Date, maxAgeSeconds = 300): void {
  const secret = keys.get(message.keyId);
  if (!secret) throw new SecurityError("unknown key id");
  const age = Math.abs(now.getTime() - Date.parse(message.timestamp)) / 1000;
  if (!Number.isFinite(age) || age > maxAgeSeconds) throw new SecurityError("signature timestamp outside freshness window");
  const mac = createHmac("sha256", secret).update(`${message.timestamp}\n`).update(message.body).digest("hex");
  const expected = new TextEncoder().encode(`sha256=${mac}`);
  const actual = new TextEncoder().encode(message.signature);
  if (expected.length !== actual.length || !timingSafeEqual(expected, actual)) throw new SecurityError("invalid signature");
}
