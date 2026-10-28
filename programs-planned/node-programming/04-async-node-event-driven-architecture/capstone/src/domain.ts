export const TASK_HARBOR_VERSION = 'TASK_HARBOR_V1' as const;
export const PROGRAM_VERSION = '1.0.0' as const;
export type Priority = 'low' | 'normal' | 'high';

interface TaskBase {
  readonly id: string;
  readonly dependsOn: readonly string[];
  readonly priority: Priority;
  readonly timeoutMs?: number;
}
export interface DelayTask extends TaskBase { readonly kind: 'delay'; readonly milliseconds: number; }
export interface EchoTask extends TaskBase { readonly kind: 'echo'; readonly text: string; }
export interface UppercaseTask extends TaskBase { readonly kind: 'uppercase'; readonly text: string; }
export interface FailTask extends TaskBase { readonly kind: 'fail'; readonly message: string; }
export type TaskSpec = DelayTask | EchoTask | UppercaseTask | FailTask;
export interface TaskManifest { readonly version: typeof TASK_HARBOR_VERSION; readonly tasks: readonly TaskSpec[]; }
export type FailurePolicy = 'continue' | 'fail-fast';

export type TaskOutcome =
  | { readonly id: string; readonly index: number; readonly status: 'succeeded'; readonly value: string; readonly durationMs: number }
  | { readonly id: string; readonly index: number; readonly status: 'failed'; readonly error: unknown; readonly durationMs: number }
  | { readonly id: string; readonly index: number; readonly status: 'timed-out'; readonly error: unknown; readonly durationMs: number }
  | { readonly id: string; readonly index: number; readonly status: 'cancelled'; readonly reason: unknown; readonly durationMs: number }
  | { readonly id: string; readonly index: number; readonly status: 'blocked'; readonly blockedBy: readonly string[]; readonly durationMs: 0 };

export interface RunSummary {
  readonly runId: string;
  readonly policy: FailurePolicy;
  readonly outcomes: readonly TaskOutcome[];
  readonly peakConcurrency: number;
  readonly durationMs: number;
}

export function priorityRank(priority: Priority): number {
  switch (priority) {
    case 'high': return 2;
    case 'normal': return 1;
    case 'low': return 0;
  }
}
