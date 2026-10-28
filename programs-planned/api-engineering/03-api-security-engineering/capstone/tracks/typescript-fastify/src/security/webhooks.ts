import { createHash, createHmac, timingSafeEqual } from "node:crypto";
import { SecurityControlError } from "./errors.js";
import { SecretBytes } from "./secrets.js";

export function signingInput(input: { timestamp: number; deliveryId: string; keyId: string; body: Uint8Array }): Uint8Array {
  const digest = createHash("sha256").update(input.body).digest("hex");
  return new TextEncoder().encode(`v1\n${input.timestamp}\n${input.deliveryId}\n${input.keyId}\n${digest}`);
}
export function signWebhook(input: { secret: SecretBytes; timestamp: number; deliveryId: string; keyId: string; body: Uint8Array }): string {
  return `sha256=${createHmac("sha256", input.secret.reveal()).update(signingInput(input)).digest("hex")}`;
}
export class MemoryReplayStore { readonly accepted = new Set<string>(); claim(keyId: string, deliveryId: string): boolean { const key=`${keyId}\n${deliveryId}`; if(this.accepted.has(key)) return false; this.accepted.add(key); return true; } }
export function verifyWebhook(input: { body: Uint8Array; timestamp: number; deliveryId: string; keyId: string; signature: string; now: number; keys: ReadonlyMap<string, SecretBytes>; replay: MemoryReplayStore; maxAgeSeconds?: number; futureSkewSeconds?: number }): void {
  const maxAge=input.maxAgeSeconds??300; const skew=input.futureSkewSeconds??30;
  if(input.timestamp<input.now-maxAge || input.timestamp>input.now+skew) throw new SecurityControlError("webhook-stale","webhook timestamp is outside the accepted window",401);
  const secret=input.keys.get(input.keyId); if(secret===undefined) throw new SecurityControlError("webhook-key","webhook key identifier is not recognized",401);
  const expected=Buffer.from(signWebhook({secret,timestamp:input.timestamp,deliveryId:input.deliveryId,keyId:input.keyId,body:input.body}),"utf8"); const actual=Buffer.from(input.signature,"utf8");
  if(expected.length!==actual.length || !timingSafeEqual(expected,actual)) throw new SecurityControlError("webhook-signature","webhook signature is invalid",401);
  if(!input.replay.claim(input.keyId,input.deliveryId)) throw new SecurityControlError("webhook-replay","webhook delivery identifier was already accepted",409);
}
