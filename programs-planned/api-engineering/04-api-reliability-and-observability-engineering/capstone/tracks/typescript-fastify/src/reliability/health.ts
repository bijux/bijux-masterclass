export type LifecyclePhase =
  | "starting"
  | "accepting"
  | "draining"
  | "stopped"
  | "failed";

export interface LifecycleTransition {
  readonly fromPhase: LifecyclePhase;
  readonly toPhase: LifecyclePhase;
  readonly reason: string;
  readonly timestampMs: number;
}

const ALLOWED: Readonly<Record<LifecyclePhase, readonly LifecyclePhase[]>> = {
  starting: ["accepting", "draining", "failed"],
  accepting: ["draining", "failed"],
  draining: ["stopped", "failed"],
  failed: ["stopped"],
  stopped: [],
};

export class LifecycleController {
  public readonly history: LifecycleTransition[] = [];
  public constructor(public phase: LifecyclePhase = "starting") {}
  public transition(
    toPhase: LifecyclePhase,
    input: { reason: string; timestampMs: number },
  ): LifecycleTransition {
    if (input.reason.length < 1 || input.reason.length > 120) {
      throw new Error("transition reason must contain 1..120 characters");
    }
    if (!ALLOWED[this.phase].includes(toPhase)) {
      throw new Error(`invalid lifecycle transition ${this.phase}->${toPhase}`);
    }
    const item = {
      fromPhase: this.phase,
      toPhase,
      reason: input.reason,
      timestampMs: input.timestampMs,
    } as const;
    this.phase = toPhase;
    this.history.push(item);
    return item;
  }
}

export interface ComponentHealth {
  readonly name: string;
  readonly requiredForReadiness: boolean;
  readonly available: boolean;
  readonly detail?: string;
}
export interface HealthSnapshot {
  readonly live: boolean;
  readonly ready: boolean;
  readonly startupComplete: boolean;
  readonly phase: LifecyclePhase;
  readonly reasons: readonly string[];
}

export function evaluateHealth(input: {
  phase: LifecyclePhase;
  startupComplete: boolean;
  eventLoopProgressing: boolean;
  components: readonly ComponentHealth[];
}): HealthSnapshot {
  const reasons: string[] = [];
  const live = !["stopped", "failed"].includes(input.phase) &&
    input.eventLoopProgressing;
  if (!live) reasons.push("process-cannot-make-progress");
  if (input.phase === "failed") reasons.push("lifecycle-failed");
  if (!input.startupComplete) reasons.push("startup-incomplete");
  const unavailable = input.components.filter(
    (value) => value.requiredForReadiness && !value.available,
  );
  for (const component of unavailable) {
    reasons.push(`required-component-unavailable:${component.name}`);
  }
  const ready = live && input.startupComplete &&
    input.phase === "accepting" && unavailable.length === 0;
  if (input.phase === "draining") reasons.push("draining");
  return {
    live,
    ready,
    startupComplete: input.startupComplete,
    phase: input.phase,
    reasons,
  };
}
