export class UsageError extends Error {
  constructor(message: string) { super(message); this.name = 'UsageError'; }
}
export class ManifestError extends Error {
  constructor(message: string) { super(message); this.name = 'ManifestError'; }
}
export class GraphError extends Error {
  constructor(message: string) { super(message); this.name = 'GraphError'; }
}
export class TaskExecutionError extends Error {
  constructor(readonly taskId: string, message: string) {
    super(message); this.name = 'TaskExecutionError';
  }
}
export class TaskTimeoutError extends Error {
  constructor(readonly taskId: string, readonly milliseconds: number) {
    super(`task ${taskId} exceeded ${milliseconds}ms`); this.name = 'TaskTimeoutError';
  }
}
export class RunTimeoutError extends Error {
  constructor(readonly milliseconds: number) {
    super(`run exceeded ${milliseconds}ms`); this.name = 'RunTimeoutError';
  }
}
export class FailFastError extends Error {
  constructor(readonly taskId: string) {
    super(`fail-fast triggered by ${taskId}`); this.name = 'FailFastError';
  }
}
export class EventOverflowError extends Error {
  constructor(readonly capacity: number) {
    super(`event consumer exceeded capacity ${capacity}`); this.name = 'EventOverflowError';
  }
}

export function describeError(error: unknown): string {
  if (error instanceof Error) return `${error.name}: ${error.message}`;
  if (typeof error === 'string') return error;
  try { return JSON.stringify(error); } catch { return String(error); }
}
