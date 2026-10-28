import type { EventEnvelope } from "./envelope.js";

export interface RunProcessState {
  runId: string;
  status: "new" | "start-requested" | "requested" | "running" | "completed" | "failed" | "reconcile-start";
  generation: number;
  lastEventId: string | null;
  commandId: string | null;
}

export function initialRunProcess(runId: string): RunProcessState {
  if (!runId) throw new Error("runId cannot be blank");
  return { runId, status: "new", generation: 0, lastEventId: null, commandId: null };
}

export class RunProcessManager {
  apply(state: RunProcessState, event: EventEnvelope): "applied" | "duplicate" | "ignored" {
    if (state.lastEventId === event.id) return "duplicate";
    const eventType = event.type;
    if (eventType.endsWith("run.requested.v1")) {
      if (state.status === "new") {
        state.status = "start-requested";
        state.generation += 1;
        state.commandId = `start:${state.runId}:${state.generation}`;
      }
    } else if (eventType.endsWith("run.started.v1")) {
      if (state.status === "start-requested" || state.status === "requested") state.status = "running";
      else if (!["running", "completed", "failed"].includes(state.status)) throw new Error("started event violates process state");
    } else if (eventType.endsWith("run.completed.v1")) {
      if (state.status === "running" || state.status === "start-requested") state.status = "completed";
      else if (state.status !== "completed") throw new Error("completed event violates process state");
    } else if (eventType.endsWith("run.failed.v1")) {
      if (state.status !== "completed" && state.status !== "failed") state.status = "failed";
    } else return "ignored";
    state.lastEventId = event.id;
    return "applied";
  }

  timeout(state: RunProcessState, generation: number): "applied" | "stale" | "ignored" {
    if (generation !== state.generation || state.status === "completed" || state.status === "failed") return "stale";
    if (state.status === "start-requested") {
      state.status = "reconcile-start";
      return "applied";
    }
    return "ignored";
  }
}
