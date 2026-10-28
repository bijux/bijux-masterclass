export type FaultKind = "delay" | "error" | "drop" | "corrupt";
export interface FaultRule { readonly target: string; readonly kind: FaultKind; readonly probability: number; readonly delayMs?: number; readonly errorCode?: string }
function rng(seed: number): () => number { let state = seed >>> 0; return () => { state = (Math.imul(1664525, state) + 1013904223) >>> 0; return state / 0x100000000; }; }
export class FaultInjector {
  private readonly random: () => number;
  public constructor(private readonly rules: readonly FaultRule[], seed = 0) { this.random = rng(seed); }
  public decide(target: string): FaultRule | undefined { return this.rules.find((rule) => rule.target === target && this.random() < rule.probability); }
}

export interface FaultPlanInput {
  readonly id: string;
  readonly hypothesis: string;
  readonly steadyState: readonly string[];
  readonly blastRadius: string;
  readonly abortConditions: readonly string[];
  readonly cleanup: readonly string[];
  readonly approvedEnvironments?: readonly string[];
}

export class FaultPlan {
  public constructor(public readonly input: FaultPlanInput) {}
  public validate(): void {
    if (this.input.id.length < 1 || this.input.id.length > 80) {
      throw new Error("fault plan identifier must contain 1..80 characters");
    }
    if (this.input.hypothesis.trim().length < 12) {
      throw new Error("fault plan requires a falsifiable hypothesis");
    }
    if (this.input.steadyState.length === 0) throw new Error("fault plan requires a steady-state definition");
    if (this.input.blastRadius.trim() === "") throw new Error("fault plan requires a blast radius");
    if (this.input.abortConditions.length === 0) throw new Error("fault plan requires abort conditions");
    if (this.input.cleanup.length === 0) throw new Error("fault plan requires cleanup actions");
    if ((this.input.approvedEnvironments ?? ["course", "test"]).length === 0) {
      throw new Error("fault plan requires approved environments");
    }
  }
}

