import type { EventEnvelope } from "./envelope.js";
import { DeterministicBroker } from "./broker.js";

export interface OutboxRow {
  readonly eventId: string;
  readonly channel: string;
  readonly key: string;
  readonly event: EventEnvelope;
  state: "pending" | "published";
  attempts: number;
  publishedAtMs?: number;
}

export class DomainOutboxStore {
  readonly domain = new Map<string, Record<string, unknown>>();
  readonly outbox = new Map<string, OutboxRow>();

  commit(input: { aggregateId: string; aggregateState: Record<string, unknown>; channel: string; key: string; event: EventEnvelope }): void {
    if (this.outbox.has(input.event.id)) throw new Error("duplicate outbox event id");
    this.domain.set(input.aggregateId, { ...input.aggregateState });
    this.outbox.set(input.event.id, {
      eventId: input.event.id,
      channel: input.channel,
      key: input.key,
      event: input.event,
      state: "pending",
      attempts: 0,
    });
  }

  pending(): OutboxRow[] {
    return [...this.outbox.values()].filter((row) => row.state === "pending").sort((a, b) => a.eventId.localeCompare(b.eventId));
  }
}

export class OutboxRelay {
  constructor(private readonly store: DomainOutboxStore, private readonly broker: DeterministicBroker, private readonly clock: () => number = () => Date.now()) {}

  step(crashAfterPublish = false): "idle" | "published" {
    const row = this.store.pending()[0];
    if (!row) return "idle";
    row.attempts += 1;
    this.broker.publish(row.channel, row.key, row.event);
    if (crashAfterPublish) throw new Error("injected crash after broker acceptance");
    row.state = "published";
    row.publishedAtMs = this.clock();
    return "published";
  }
}
