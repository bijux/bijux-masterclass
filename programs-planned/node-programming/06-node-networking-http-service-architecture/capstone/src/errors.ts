export type ProblemCode =
  | 'ROUTE_NOT_FOUND'
  | 'METHOD_NOT_ALLOWED'
  | 'UNSUPPORTED_MEDIA_TYPE'
  | 'BODY_REQUIRED'
  | 'BODY_TOO_LARGE'
  | 'MALFORMED_JSON'
  | 'INVALID_REQUEST'
  | 'IDEMPOTENCY_KEY_REQUIRED'
  | 'IDEMPOTENCY_CONFLICT'
  | 'JOB_NOT_FOUND'
  | 'PRECONDITION_FAILED'
  | 'OVER_CAPACITY'
  | 'NOT_READY'
  | 'REPLAY_GAP'
  | 'INTERNAL';

export interface Problem {
  readonly type: string;
  readonly title: string;
  readonly status: number;
  readonly code: ProblemCode;
  readonly detail: string;
  readonly requestId: string;
}

export class ServiceProblem extends Error {
  constructor(
    readonly code: ProblemCode,
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = 'ServiceProblem';
  }
}

export function toProblem(error: unknown, requestId: string): Problem {
  const source = error instanceof ServiceProblem
    ? error
    : new ServiceProblem('INTERNAL', 500, 'Internal service failure');
  const slug = source.code.toLowerCase().replaceAll('_', '-');
  return {
    type: `https://servicewire.invalid/problems/${slug}`,
    title: source.message.slice(0, 160),
    status: source.status,
    code: source.code,
    detail: source.message.slice(0, 240),
    requestId,
  };
}
