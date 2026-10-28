export interface Principal {
  subject: string;
  tenantId: string;
  permissions: ReadonlySet<string>;
}

export interface RequestContext {
  principal: Principal;
  requestId: string;
  deadlineMs: number;
  clientName: string;
  nowEpoch: number;
}

export interface GraphError {
  message: string;
  path?: readonly (string | number)[];
  code: string;
  service?: string;
  details?: Readonly<Record<string, unknown>>;
}

export interface ExecutionResult {
  data: Record<string, unknown> | null;
  errors?: readonly GraphError[];
  extensions?: Readonly<Record<string, unknown>>;
}

export class ValidationError extends Error {}
export class AuthorizationError extends Error {}
export class ConflictError extends Error {}
export class PreconditionFailed extends Error {}

export class DownstreamUnavailable extends Error {
  constructor(readonly service: string, message = "downstream unavailable") {
    super(message);
  }
}
