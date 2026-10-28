import { envelopeBytes, type EventEnvelope } from "./envelope.js";

export interface NatsPublishRequest {
  readonly subject: string;
  readonly payload: Uint8Array;
  readonly headers: Readonly<Record<string, string>>;
  readonly messageId: string;
}

export interface JetStreamPublisher {
  publish(
    subject: string,
    payload: Uint8Array,
    options: { msgID: string; headers: Readonly<Record<string, string>> },
  ): Promise<unknown>;
}

export function toNatsRequest(subject: string, event: EventEnvelope): NatsPublishRequest {
  if (!subject || /\s/.test(subject)) throw new Error("invalid NATS subject");
  return {
    subject,
    payload: envelopeBytes(event),
    headers: {
      "Content-Type": "application/cloudevents+json",
      "X-Event-Type": event.type,
      "X-Tenant-Id": event.tenantid,
    },
    messageId: event.id,
  };
}

export async function publishJetStream(
  client: JetStreamPublisher,
  request: NatsPublishRequest,
): Promise<unknown> {
  return client.publish(request.subject, request.payload, {
    msgID: request.messageId,
    headers: request.headers,
  });
}
