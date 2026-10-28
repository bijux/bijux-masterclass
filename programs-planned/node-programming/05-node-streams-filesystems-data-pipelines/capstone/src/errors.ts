export type FlowErrorCode =
  | 'USAGE'
  | 'IO'
  | 'DECODE'
  | 'SOURCE_LIMIT'
  | 'LINE_LIMIT'
  | 'JSON_SYNTAX'
  | 'EVENT_SCHEMA'
  | 'EVENT_LIMIT'
  | 'EXPANDED_LIMIT'
  | 'OUTPUT_LIMIT'
  | 'DIGEST_MISMATCH'
  | 'CHILD_FAILED'
  | 'CHILD_OUTPUT_LIMIT'
  | 'COMMIT';

export class FlowError extends Error {
  constructor(
    readonly code: FlowErrorCode,
    message: string,
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = 'FlowError';
  }
}

export class UsageError extends FlowError {
  constructor(message: string) {
    super('USAGE', message);
    this.name = 'UsageError';
  }
}

export function asFlowError(
  error: unknown,
  code: FlowErrorCode,
  message: string,
): FlowError {
  return error instanceof FlowError
    ? error
    : new FlowError(code, message, { cause: error });
}
