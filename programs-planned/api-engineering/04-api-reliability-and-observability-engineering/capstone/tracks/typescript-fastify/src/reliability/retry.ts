import type { Clock } from "./clock.js";
import type { Deadline } from "./deadline.js";

export type RetrySafety = "safe" | "idempotent" | "idempotency-key" | "unsafe";

export interface RetryPolicy {
  readonly maxAttempts: number;
  readonly initialDelayMs: number;
  readonly maximumDelayMs: number;
  readonly multiplier: number;
  readonly jitter: "none" | "full";
}

const RETRYABLE = new Set([408, 425, 429, 500, 502, 503, 504]);

export function retryable(input: {
  status?: number;
  transportError: boolean;
  safety: RetrySafety;
}): boolean {
  if (input.safety === "unsafe") return false;
  return input.transportError ||
    (input.status !== undefined && RETRYABLE.has(input.status));
}

function validatePolicy(policy: RetryPolicy): void {
  if (!Number.isSafeInteger(policy.maxAttempts) || policy.maxAttempts < 1) {
    throw new Error("maxAttempts must be a positive safe integer");
  }
  if (policy.initialDelayMs < 0 || policy.maximumDelayMs < 0) {
    throw new Error("delays must be non-negative");
  }
  if (policy.maximumDelayMs < policy.initialDelayMs) {
    throw new Error("maximumDelayMs must not be below initialDelayMs");
  }
  if (!Number.isFinite(policy.multiplier) || policy.multiplier < 1) {
    throw new Error("multiplier must be at least one");
  }
}

function rng(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(1664525, state) + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

export function parseRetryAfterMs(
  value: string | undefined,
  nowMs = Date.now(),
): number | undefined {
  if (value === undefined) return undefined;
  const raw = value.trim();
  if (/^[0-9]+$/.test(raw)) {
    const seconds = Number(raw);
    if (!Number.isSafeInteger(seconds)) return undefined;
    return seconds * 1000;
  }
  const timestamp = Date.parse(raw);
  if (!Number.isFinite(timestamp)) return undefined;
  return Math.max(0, Math.trunc(timestamp - nowMs));
}

export function planRetryDelays(
  policy: RetryPolicy,
  seed = 0,
  floors: readonly (number | undefined)[] = [],
): number[] {
  validatePolicy(policy);
  const random = rng(seed);
  const delays: number[] = [];
  for (let index = 0; index < policy.maxAttempts - 1; index += 1) {
    const cap = Math.min(
      policy.maximumDelayMs,
      Math.floor(policy.initialDelayMs * policy.multiplier ** index),
    );
    let delay = policy.jitter === "none"
      ? cap
      : Math.floor(random() * (cap + 1));
    const floor = floors[index];
    if (floor !== undefined) {
      if (!Number.isFinite(floor) || floor < 0) {
        throw new Error("server delay floor must be non-negative");
      }
      delay = Math.max(delay, floor);
    }
    delays.push(delay);
  }
  return delays;
}

export function fitDelaysToDeadline(
  delays: readonly number[],
  input: {
    clock: Clock;
    deadline: Deadline;
    minimumAttemptMs: number;
  },
): number[] {
  if (!Number.isFinite(input.minimumAttemptMs) || input.minimumAttemptMs <= 0) {
    throw new Error("minimumAttemptMs must be positive");
  }
  let remaining = input.deadline.remainingMs(input.clock);
  const accepted: number[] = [];
  for (const delay of delays) {
    if (!Number.isFinite(delay) || delay < 0) {
      throw new Error("retry delay must be non-negative");
    }
    const required = delay + input.minimumAttemptMs;
    if (required > remaining) break;
    accepted.push(delay);
    remaining -= required;
  }
  return accepted;
}
