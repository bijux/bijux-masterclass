import { randomUUID } from "node:crypto";
import { DeterministicBroker } from "./broker.js";
import type { EventEnvelope } from "./envelope.js";

export interface DeadLetter { id: string; tenantId: string; consumer: string; originalEvent: EventEnvelope; channel: string; partition: number; offset: string; attempts: number; failureCode: string; safeDetail: string }
export class DeadLetterStore { readonly rows: DeadLetter[] = []; append(row: DeadLetter): void { this.rows.push(row); } }
export class PermanentMessageError extends Error {}

export class ConsumerRunner {
  constructor(private readonly broker: DeterministicBroker, private readonly deadLetters: DeadLetterStore, private readonly maxAttempts = 3, private readonly retryDelayMs: (attempt: number) => number = (attempt) => attempt * 1000) {
    if (maxAttempts <= 0) throw new Error("maxAttempts must be positive");
  }

  step(group: string, channel: string, handler: (event: EventEnvelope) => void): "idle" | "acked" | "retry" | "dead-lettered" {
    const delivery = this.broker.poll(group, channel, 1, 10_000)[0];
    if (!delivery) return "idle";
    try { handler(delivery.record.event); }
    catch (error) {
      const failure = error instanceof Error ? error : new Error(String(error));
      if (failure instanceof PermanentMessageError || delivery.attempt >= this.maxAttempts) {
        this.deadLetters.append({ id: randomUUID(), tenantId: delivery.record.event.tenantid, consumer: group, originalEvent: delivery.record.event, channel, partition: delivery.record.partition, offset: delivery.record.offset, attempts: delivery.attempt, failureCode: failure.constructor.name, safeDetail: failure.message.slice(0, 256) });
        this.broker.term(delivery.token);
        return "dead-lettered";
      }
      this.broker.nack(delivery.token, this.retryDelayMs(delivery.attempt));
      return "retry";
    }
    this.broker.ack(delivery.token);
    return "acked";
  }
}

export interface LagHealth { state: "healthy" | "warning" | "critical"; lag: number; oldestAgeSeconds: number }
export function classifyLag(lag: number, oldestAgeSeconds: number, policy: { warningLag: number; criticalLag: number; warningAge: number; criticalAge: number }): LagHealth {
  const values = [lag, oldestAgeSeconds, policy.warningLag, policy.criticalLag, policy.warningAge, policy.criticalAge];
  if (values.some((value) => value < 0)) throw new Error("lag values cannot be negative");
  if (policy.criticalLag < policy.warningLag || policy.criticalAge < policy.warningAge) throw new Error("invalid thresholds");
  const state = lag >= policy.criticalLag || oldestAgeSeconds >= policy.criticalAge ? "critical" : lag >= policy.warningLag || oldestAgeSeconds >= policy.warningAge ? "warning" : "healthy";
  return { state, lag, oldestAgeSeconds };
}
