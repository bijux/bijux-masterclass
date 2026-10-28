export type RunState =
  | "queued"
  | "running"
  | "completed"
  | "failed"
  | "canceled";

export type RunSnapshot = Readonly<{
  state: RunState;
  progress: number;
  cancellationRequested: boolean;
}>;

const transitions: Readonly<Record<RunState, ReadonlySet<RunState>>> = {
  queued: new Set(["running", "canceled"]),
  running: new Set(["completed", "failed", "canceled"]),
  completed: new Set(),
  failed: new Set(),
  canceled: new Set(),
};

export class DomainError extends Error {
  public constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = "DomainError";
  }
}

/**
 * Course-wide deterministic JSON profile.
 *
 * This is intentionally not presented as RFC 8785/JCS. It accepts null, strings, booleans, JavaScript-safe integers, arrays, and
 * string-keyed objects. It sorts names by Unicode code point, preserves array
 * order, rejects floating-point values, and omits undefined object members in
 * the same way a parsed JSON request omits an absent property.
 */
function compareUnicodeCodePoints(left: string, right: string): number {
  const leftPoints = Array.from(left, (value) => value.codePointAt(0)!);
  const rightPoints = Array.from(right, (value) => value.codePointAt(0)!);
  const count = Math.min(leftPoints.length, rightPoints.length);
  for (let index = 0; index < count; index += 1) {
    const difference = leftPoints[index]! - rightPoints[index]!;
    if (difference !== 0) return difference;
  }
  return leftPoints.length - rightPoints.length;
}

export function canonicalJson(value: unknown): string {
  if (value === null) return "null";
  if (typeof value === "string" || typeof value === "boolean") {
    return JSON.stringify(value);
  }
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) {
      throw new TypeError(
        "canonical JSON profile accepts only JavaScript-safe integers",
      );
    }
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    if (value.some((item) => item === undefined)) {
      throw new TypeError("canonical JSON rejects undefined array elements");
    }
    return `[${value.map(canonicalJson).join(",")}]`;
  }
  if (typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>)
      .filter(([, member]) => member !== undefined)
      .sort(([left], [right]) => compareUnicodeCodePoints(left, right));
    return `{${entries
      .map(([key, member]) => `${JSON.stringify(key)}:${canonicalJson(member)}`)
      .join(",")}}`;
  }
  throw new TypeError(`unsupported canonical JSON value: ${typeof value}`);
}

export function projectEtag(projectId: string, version: number): string {
  if (!Number.isSafeInteger(version) || version < 1) {
    throw new TypeError("version must be a positive safe integer");
  }
  return `"${projectId}:${version}"`;
}

export function parseProjectEtag(value: string, projectId: string): number {
  const escaped = projectId.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = new RegExp(`^"${escaped}:([0-9]+)"$`).exec(value);
  if (!match) {
    throw new DomainError(
      "precondition-failed",
      "entity tag does not identify this project",
    );
  }
  const version = Number(match[1]);
  if (!Number.isSafeInteger(version) || version < 1 || version > 2_147_483_647) {
    throw new DomainError("precondition-failed", "entity tag is malformed");
  }
  return version;
}

export function parseCursor(value: string | undefined): string | undefined {
  if (value === undefined) return undefined;
  if (!/^[1-9][0-9]{0,18}$/.test(value)) {
    throw new DomainError(
      "cursor-invalid",
      "cursor must be a positive signed-64-bit decimal handle",
    );
  }
  if (BigInt(value) > 9_223_372_036_854_775_807n) {
    throw new DomainError(
      "cursor-invalid",
      "cursor exceeds PostgreSQL signed-bigint range",
    );
  }
  return value;
}

export function requireTransition(current: RunState, target: RunState): void {
  if (!transitions[current].has(target)) {
    throw new DomainError(
      "invalid-run-transition",
      `analysis run cannot move from ${current} to ${target}`,
    );
  }
}

export function evolve(
  snapshot: RunSnapshot,
  command:
    | "claim"
    | "complete"
    | "fail"
    | "request-cancel"
    | "observe-cancel",
): RunSnapshot {
  if (command === "request-cancel") {
    if (["completed", "failed", "canceled"].includes(snapshot.state)) {
      throw new DomainError(
        "invalid-run-transition",
        "terminal run cannot be canceled",
      );
    }
    return { ...snapshot, cancellationRequested: true };
  }
  const target: RunState =
    command === "claim"
      ? "running"
      : command === "complete"
        ? "completed"
        : command === "fail"
          ? "failed"
          : "canceled";
  requireTransition(snapshot.state, target);
  return {
    state: target,
    progress:
      target === "running"
        ? 10
        : target === "completed"
          ? 100
          : snapshot.progress,
    cancellationRequested: snapshot.cancellationRequested,
  };
}

export function retryDelaySeconds(attempt: number, cap = 300): number {
  if (!Number.isSafeInteger(attempt) || attempt < 1) {
    throw new TypeError("attempt is one-based");
  }
  return Math.min(cap, 2 ** Math.min(attempt - 1, 12));
}
