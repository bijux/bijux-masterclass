export type ErrorCode =
  | 'COMMAND_INVALID'
  | 'DOMAIN_INVALID'
  | 'DOMAIN_MISSING'
  | 'DOMAIN_TRANSITION'
  | 'STORAGE_INVALID'
  | 'STORAGE_IO';

export abstract class StudyLedgerError extends Error {
  abstract readonly code: ErrorCode;

  protected constructor(message: string, options?: ErrorOptions) {
    super(message, options);
  }
}

export class CommandError extends StudyLedgerError {
  override readonly name = 'CommandError';
  override readonly code = 'COMMAND_INVALID' as const;

  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
  }
}

export class DomainError extends StudyLedgerError {
  override readonly name = 'DomainError';

  constructor(
    override readonly code: 'DOMAIN_INVALID' | 'DOMAIN_MISSING' | 'DOMAIN_TRANSITION',
    message: string,
    options?: ErrorOptions,
  ) {
    super(message, options);
  }
}

export interface ValidationIssue {
  readonly path: string;
  readonly message: string;
}

export class StorageValidationError extends StudyLedgerError {
  override readonly name = 'StorageValidationError';
  override readonly code = 'STORAGE_INVALID' as const;

  constructor(readonly issues: readonly ValidationIssue[], options?: ErrorOptions) {
    super(
      issues.length === 1
        ? `invalid ledger: ${issues[0]?.path ?? '$'}: ${issues[0]?.message ?? 'unknown issue'}`
        : `invalid ledger: ${issues.length} validation issues`,
      options,
    );
  }
}

export class StorageIoError extends StudyLedgerError {
  override readonly name = 'StorageIoError';
  override readonly code = 'STORAGE_IO' as const;

  constructor(readonly operation: string, readonly path: string, options?: ErrorOptions) {
    super(`cannot ${operation} ledger at ${path}`, options);
  }
}
