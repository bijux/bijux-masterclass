export interface FlowLimits {
  readonly maxSourceBytes: number;
  readonly maxLineBytes: number;
  readonly maxEvents: number;
  readonly maxExpandedBytes: number;
  readonly maxOutputBytes: number;
  readonly maxIdBytes: number;
  readonly maxKindBytes: number;
  readonly maxChildOutputBytes: number;
  readonly maxChildStderrBytes: number;
}

export const DEFAULT_LIMITS: FlowLimits = Object.freeze({
  maxSourceBytes: 512 * 1024 * 1024,
  maxLineBytes: 64 * 1024,
  maxEvents: 1_000_000,
  maxExpandedBytes: 512 * 1024 * 1024,
  maxOutputBytes: 512 * 1024 * 1024,
  maxIdBytes: 256,
  maxKindBytes: 128,
  maxChildOutputBytes: 512 * 1024 * 1024,
  maxChildStderrBytes: 64 * 1024,
});
