import { canonicalBytes } from "./canonical.js";

const TYPE_RE = /^[a-z0-9]+(?:[.-][a-z0-9]+)*\.v[1-9][0-9]*$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const TRACE_RE = /^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$/;

export class EnvelopeError extends Error {}

export interface EventEnvelope {
  readonly specversion: "1.0";
  readonly id: string;
  readonly source: string;
  readonly type: string;
  readonly subject: string;
  readonly time: string;
  readonly datacontenttype: "application/json";
  readonly dataschema: string;
  readonly tenantid: string;
  readonly correlationid: string;
  readonly causationid: string | null;
  readonly partitionkey: string;
  readonly data: Readonly<Record<string, unknown>>;
  readonly traceparent?: string;
}

function absoluteUri(value: string, field: string): void {
  try {
    const parsed = new URL(value);
    if (!parsed.protocol) throw new Error();
  } catch {
    // URL does not accept all URNs in every runtime consistently; allow profile URNs.
    if (!/^urn:[a-z0-9][a-z0-9-]*:/i.test(value)) {
      throw new EnvelopeError(`${field} must be an absolute URI`);
    }
  }
}

export function validateEnvelope(event: EventEnvelope): EventEnvelope {
  if (event.specversion !== "1.0") throw new EnvelopeError("unsupported specversion");
  if (!UUID_RE.test(event.id)) throw new EnvelopeError("id must be a UUID");
  if (!UUID_RE.test(event.correlationid)) throw new EnvelopeError("correlationid must be a UUID");
  if (event.causationid !== null && !UUID_RE.test(event.causationid)) throw new EnvelopeError("causationid must be a UUID or null");
  absoluteUri(event.source, "source");
  absoluteUri(event.dataschema, "dataschema");
  if (!TYPE_RE.test(event.type)) throw new EnvelopeError("invalid event type");
  if (!event.subject || event.subject.length > 256) throw new EnvelopeError("invalid subject");
  if (!event.tenantid || event.tenantid.length > 128) throw new EnvelopeError("invalid tenantid");
  if (!event.partitionkey || event.partitionkey.length > 256) throw new EnvelopeError("invalid partitionkey");
  if (event.traceparent !== undefined && !TRACE_RE.test(event.traceparent)) throw new EnvelopeError("invalid traceparent");
  if (Number.isNaN(Date.parse(event.time))) throw new EnvelopeError("invalid time");
  canonicalBytes(event);
  return Object.freeze(event);
}

export interface BuildEventInput {
  source: string;
  eventType: string;
  subject: string;
  dataSchema: string;
  tenantId: string;
  correlationId: string;
  partitionKey: string;
  data: Record<string, unknown>;
  eventId: string;
  time: Date;
  causationId?: string | null;
  traceparent?: string;
}

export function buildEvent(input: BuildEventInput): EventEnvelope {
  const base: EventEnvelope = {
    specversion: "1.0",
    id: input.eventId.toLowerCase(),
    source: input.source,
    type: input.eventType,
    subject: input.subject,
    time: input.time.toISOString().replace(".000Z", ".000Z"),
    datacontenttype: "application/json",
    dataschema: input.dataSchema,
    tenantid: input.tenantId,
    correlationid: input.correlationId.toLowerCase(),
    causationid: input.causationId ?? null,
    partitionkey: input.partitionKey,
    data: Object.freeze({ ...input.data }),
    ...(input.traceparent === undefined ? {} : { traceparent: input.traceparent }),
  };
  return validateEnvelope(base);
}

export function envelopeBytes(event: EventEnvelope): Uint8Array {
  return canonicalBytes(event);
}
