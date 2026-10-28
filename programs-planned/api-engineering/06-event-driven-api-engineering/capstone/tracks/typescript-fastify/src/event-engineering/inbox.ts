import type { EventEnvelope } from "./envelope.js";

export interface ProcessResult { readonly status: "applied" | "duplicate"; readonly revision: number }

export class TransactionalProjection {
  private readonly seen = new Map<string, number>();
  private readonly states = new Map<string, Record<string, unknown>>();
  private revision = 0;

  apply(input: {
    tenantId: string;
    consumer: string;
    effectVersion: string;
    event: EventEnvelope;
    mutation: (state: Record<string, unknown>, event: EventEnvelope) => void;
  }): ProcessResult {
    const identity = `${input.tenantId}\u0000${input.consumer}\u0000${input.effectVersion}\u0000${input.event.id}`;
    const existing = this.seen.get(identity);
    if (existing !== undefined) return { status: "duplicate", revision: existing };
    const target = `${input.tenantId}\u0000${input.consumer}:${input.effectVersion}`;
    const state = { ...(this.states.get(target) ?? {}) };
    input.mutation(state, input.event);
    this.revision += 1;
    this.states.set(target, state);
    this.seen.set(identity, this.revision);
    return { status: "applied", revision: this.revision };
  }

  snapshot(tenantId: string, consumer: string, effectVersion: string): Record<string, unknown> {
    return { ...(this.states.get(`${tenantId}\u0000${consumer}:${effectVersion}`) ?? {}) };
  }

  get appliedCount(): number { return this.seen.size; }
}
