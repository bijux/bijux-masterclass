import {
  createHash,
  createHmac,
  timingSafeEqual,
} from "node:crypto";

export {
  DomainError,
  canonicalJson,
  evolve,
  parseCursor,
  parseProjectEtag,
  projectEtag,
  requireTransition,
  retryDelaySeconds,
} from "./core/domain.js";
import { canonicalJson } from "./core/domain.js";

export function requestFingerprint(
  operationId: string,
  ownerId: string,
  body: unknown,
): string {
  return createHash("sha256")
    .update(canonicalJson({ operationId, ownerId, body }), "utf8")
    .digest("hex");
}

export function filterFingerprint(
  operationId: string,
  ownerId: string,
  filters: unknown,
): string {
  return createHash("sha256")
    .update(canonicalJson({ operationId, ownerId, filters }), "utf8")
    .digest("hex");
}

export function webhookSignature(
  secret: string,
  timestamp: string,
  body: Uint8Array,
): string {
  const digest = createHmac("sha256", secret)
    .update(timestamp, "ascii")
    .update(".")
    .update(body)
    .digest("hex");
  return `sha256=${digest}`;
}

export function verifyWebhookSignature(
  secret: string,
  timestamp: string,
  body: Uint8Array,
  candidate: string,
): boolean {
  const expected = Buffer.from(webhookSignature(secret, timestamp, body));
  const received = Buffer.from(candidate);
  return (
    expected.length === received.length &&
    timingSafeEqual(expected, received)
  );
}
