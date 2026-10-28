import { randomBytes } from "node:crypto";

export class TraceContextError extends Error {}

export interface TraceContext {
  readonly traceId: string;
  readonly spanId: string;
  readonly sampled: boolean;
  readonly remote: boolean;
}

const TRACEPARENT = /^([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$/;

export function parseTraceparent(value: string): TraceContext {
  const match = TRACEPARENT.exec(value.trim());
  if (match === null) throw new TraceContextError("malformed traceparent");
  const [, version, traceId, spanId, flags] = match;
  if (version !== "00") throw new TraceContextError("unsupported traceparent version");
  if (/^0+$/.test(traceId!) || /^0+$/.test(spanId!)) throw new TraceContextError("zero identifier");
  return { traceId: traceId!, spanId: spanId!, sampled: (Number.parseInt(flags!, 16) & 1) === 1, remote: true };
}

export function formatTraceparent(context: TraceContext): string {
  return `00-${context.traceId}-${context.spanId}-${context.sampled ? "01" : "00"}`;
}

export function newRoot(sampled = false): TraceContext {
  return { traceId: randomBytes(16).toString("hex"), spanId: randomBytes(8).toString("hex"), sampled, remote: false };
}

export function childOf(parent: TraceContext, spanId = randomBytes(8).toString("hex")): TraceContext {
  if (!/^[0-9a-f]{16}$/.test(spanId) || /^0+$/.test(spanId)) throw new TraceContextError("invalid span-id");
  return { traceId: parent.traceId, spanId, sampled: parent.sampled, remote: false };
}
