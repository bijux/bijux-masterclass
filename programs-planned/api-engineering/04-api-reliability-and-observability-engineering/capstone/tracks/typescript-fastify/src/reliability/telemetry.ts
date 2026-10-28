export const SENSITIVE_KEYS = new Set([
  "authorization", "api_key", "apikey", "password", "secret", "token",
  "access_token", "refresh_token", "webhooksecret", "webhook_secret",
  "private_key", "pepper", "cookie", "set_cookie",
]);
const BEARER = /(Bearer)\s+[A-Za-z0-9._~+/-]+={0,2}/giu;
const EVENT_NAME = /^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$/;
const SEVERITIES = new Set(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]);

function redactString(value: string): string {
  const candidate = value.replace(BEARER, "$1 [REDACTED]");
  try {
    const url = new URL(candidate);
    if (url.username !== "" || url.password !== "") {
      url.username = "[REDACTED]";
      url.password = "";
      return url.toString().replace("%5BREDACTED%5D", "[REDACTED]");
    }
  } catch {
    // Ordinary text is not required to be a URL.
  }
  return candidate;
}

export function redact(value: unknown, key?: string): unknown {
  const normalized = key?.toLowerCase().replaceAll("-", "_");
  if (normalized !== undefined &&
      (SENSITIVE_KEYS.has(normalized) ||
       SENSITIVE_KEYS.has(normalized.replaceAll("_", "")))) {
    return "[REDACTED]";
  }
  if (Array.isArray(value)) return value.map((item) => redact(item));
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .map(([name, item]) => [name, redact(item, name)]),
    );
  }
  if (typeof value === "string") return redactString(value);
  return value;
}

export interface TelemetryEvent {
  readonly timestampMs: number;
  readonly severity: string;
  readonly eventName: string;
  readonly serviceName: string;
  readonly serviceVersion: string;
  readonly deploymentEnvironment: string;
  readonly schemaVersion: string;
  readonly traceId?: string;
  readonly spanId?: string;
  readonly attributes: Readonly<Record<string, unknown>>;
}

function validateEvent(event: TelemetryEvent): void {
  if (!Number.isSafeInteger(event.timestampMs) || event.timestampMs < 0) {
    throw new Error("timestampMs must be a non-negative safe integer");
  }
  if (!SEVERITIES.has(event.severity)) throw new Error("unsupported telemetry severity");
  if (!EVENT_NAME.test(event.eventName)) {
    throw new Error("eventName must be a stable dotted identifier");
  }
  for (const [name, value] of Object.entries({
    serviceName: event.serviceName,
    serviceVersion: event.serviceVersion,
    deploymentEnvironment: event.deploymentEnvironment,
    schemaVersion: event.schemaVersion,
  })) {
    if (value.length < 1 || value.length > 120) {
      throw new Error(`${name} must contain 1..120 characters`);
    }
  }
}

export class InMemoryEventSink {
  public readonly events: TelemetryEvent[] = [];
  public dropped = 0;
  public constructor(public readonly maximumEvents = 1_000) {
    if (!Number.isSafeInteger(maximumEvents) || maximumEvents < 1) {
      throw new Error("maximumEvents must be positive");
    }
  }
  public emit(event: TelemetryEvent): boolean {
    validateEvent(event);
    if (this.events.length >= this.maximumEvents) {
      this.dropped += 1;
      return false;
    }
    this.events.push(event);
    return true;
  }
}

export interface TraceIdentity {
  readonly traceId: string;
  readonly spanId: string;
}

export class StructuredLogger {
  public constructor(
    private readonly input: {
      readonly nowMs: () => number;
      readonly sink: InMemoryEventSink;
      readonly serviceName: string;
      readonly serviceVersion: string;
      readonly deploymentEnvironment?: string;
      readonly schemaVersion?: string;
      readonly maximumAttributeBytes?: number;
    },
  ) {
    if ((input.maximumAttributeBytes ?? 32_768) < 256) {
      throw new Error("maximumAttributeBytes must be at least 256");
    }
  }

  public emit(
    eventName: string,
    input: {
      readonly severity?: string;
      readonly context?: TraceIdentity;
      readonly attributes?: Readonly<Record<string, unknown>>;
    } = {},
  ): boolean {
    let attributes = redact(input.attributes ?? {}) as Record<string, unknown>;
    const bytes = new TextEncoder().encode(JSON.stringify(attributes)).byteLength;
    if (bytes > (this.input.maximumAttributeBytes ?? 32_768)) {
      attributes = {
        "telemetry.truncated": true,
        "telemetry.original_attribute_bytes": bytes,
      };
    }
    const contextFields = input.context === undefined
      ? {}
      : { traceId: input.context.traceId, spanId: input.context.spanId };
    return this.input.sink.emit({
      timestampMs: this.input.nowMs(),
      severity: input.severity ?? "INFO",
      eventName,
      serviceName: this.input.serviceName,
      serviceVersion: this.input.serviceVersion,
      deploymentEnvironment: this.input.deploymentEnvironment ?? "development",
      schemaVersion: this.input.schemaVersion ?? "1.0",
      ...contextFields,
      attributes,
    });
  }
}

export function eventToJson(event: TelemetryEvent): string {
  return JSON.stringify(event, Object.keys(event).sort());
}
