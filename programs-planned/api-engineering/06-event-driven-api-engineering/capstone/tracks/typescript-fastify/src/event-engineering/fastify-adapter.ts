import type { EventEnvelope } from "./envelope.js";

export interface EventIngressDependencies {
  validate(body: unknown): EventEnvelope;
  dispatch(event: EventEnvelope): Promise<Record<string, unknown>>;
}

export function buildEventIngress(dependencies: EventIngressDependencies) {
  return async (body: unknown): Promise<Record<string, unknown>> => {
    const event = dependencies.validate(body);
    return dependencies.dispatch(event);
  };
}
