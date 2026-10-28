export interface ServiceLimits {
  readonly maxConnections: number;
  readonly maxHttp2Sessions: number;
  readonly maxHttp2Streams: number;
  readonly maxRequestBodyBytes: number;
  readonly maxResponseBodyBytes: number;
  readonly maxJobs: number;
  readonly maxActiveJobs: number;
  readonly maxIdempotencyRecords: number;
  readonly maxEvents: number;
  readonly maxSubscribers: number;
  readonly maxSubscriberQueueBytes: number;
  readonly maxOperationMs: number;
  readonly heartbeatMs: number;
  readonly shutdownGraceMs: number;
}

export const defaultLimits: ServiceLimits = {
  maxConnections: 32,
  maxHttp2Sessions: 8,
  maxHttp2Streams: 16,
  maxRequestBodyBytes: 64 * 1024,
  maxResponseBodyBytes: 128 * 1024,
  maxJobs: 256,
  maxActiveJobs: 8,
  maxIdempotencyRecords: 256,
  maxEvents: 512,
  maxSubscribers: 32,
  maxSubscriberQueueBytes: 64 * 1024,
  maxOperationMs: 5_000,
  heartbeatMs: 15_000,
  shutdownGraceMs: 2_000,
};

function positiveSafeInteger(name: string, value: number): void {
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new RangeError(`${name} must be a positive safe integer`);
  }
}

export function validateLimits(limits: ServiceLimits): ServiceLimits {
  for (const [name, value] of Object.entries(limits)) {
    positiveSafeInteger(name, value);
  }
  if (limits.maxActiveJobs > limits.maxJobs) {
    throw new RangeError('maxActiveJobs cannot exceed maxJobs');
  }
  if (limits.maxIdempotencyRecords < limits.maxActiveJobs) {
    throw new RangeError('maxIdempotencyRecords must cover active jobs');
  }
  if (limits.maxHttp2Streams > limits.maxConnections * 16) {
    throw new RangeError('maxHttp2Streams is inconsistent with connection capacity');
  }
  return Object.freeze({ ...limits });
}

export interface ListenConfig {
  readonly host: string;
  readonly port: number;
}

export interface TlsConfig {
  readonly key: Buffer;
  readonly cert: Buffer;
  readonly ca?: readonly Buffer[];
}

export interface RuntimeConfig {
  readonly limits: ServiceLimits;
  readonly http?: ListenConfig;
  readonly https?: ListenConfig & { readonly tls: TlsConfig };
  readonly http2?: ListenConfig;
  readonly discovery?: ListenConfig;
  readonly advertisedUrl?: string;
}

export function validateListenConfig(value: ListenConfig): ListenConfig {
  if (value.host.length === 0 || value.host.length > 255) {
    throw new RangeError('host length is invalid');
  }
  if (!Number.isInteger(value.port) || value.port < 0 || value.port > 65_535) {
    throw new RangeError('port must be between 0 and 65535');
  }
  return Object.freeze({ ...value });
}
