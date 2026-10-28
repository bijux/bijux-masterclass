import { FlowError } from './errors.js';

export interface FlowEvent {
  readonly id: string;
  readonly timestamp: string;
  readonly kind: string;
  readonly value: number;
}

export interface EventLimits {
  readonly maxIdBytes: number;
  readonly maxKindBytes: number;
}

const KEYS = ['id', 'timestamp', 'kind', 'value'] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function boundedText(
  value: unknown,
  name: string,
  maxBytes: number,
): string {
  if (typeof value !== 'string' || value.length === 0) {
    throw new FlowError('EVENT_SCHEMA', `${name} must be a non-empty string`);
  }
  if (value.includes('\0') || /[\r\n\t]/u.test(value)) {
    throw new FlowError(
      'EVENT_SCHEMA',
      `${name} contains a forbidden control character`,
    );
  }
  if (Buffer.byteLength(value, 'utf8') > maxBytes) {
    throw new FlowError(
      'EVENT_SCHEMA',
      `${name} exceeds ${maxBytes} UTF-8 bytes`,
    );
  }
  return value;
}

export function parseFlowEvent(
  value: unknown,
  limits: EventLimits,
): FlowEvent {
  if (!isRecord(value)) {
    throw new FlowError('EVENT_SCHEMA', 'event must be an object');
  }

  const actual = Object.keys(value).sort();
  const expected = [...KEYS].sort();
  if (
    actual.length !== expected.length ||
    actual.some((key, index) => key !== expected[index])
  ) {
    throw new FlowError(
      'EVENT_SCHEMA',
      `event keys must be exactly ${KEYS.join(', ')}`,
    );
  }

  const id = boundedText(value.id, 'id', limits.maxIdBytes);
  const kind = boundedText(value.kind, 'kind', limits.maxKindBytes);
  if (typeof value.timestamp !== 'string') {
    throw new FlowError('EVENT_SCHEMA', 'timestamp must be a string');
  }
  const date = new Date(value.timestamp);
  if (!Number.isFinite(date.getTime()) || date.toISOString() !== value.timestamp) {
    throw new FlowError(
      'EVENT_SCHEMA',
      'timestamp must be a canonical ISO instant',
    );
  }
  if (typeof value.value !== 'number' || !Number.isFinite(value.value)) {
    throw new FlowError('EVENT_SCHEMA', 'value must be a finite number');
  }

  return Object.freeze({
    id,
    timestamp: value.timestamp,
    kind,
    value: value.value,
  });
}

export function encodeFlowEvent(event: FlowEvent): Buffer {
  return Buffer.from(
    `${JSON.stringify({
      id: event.id,
      timestamp: event.timestamp,
      kind: event.kind,
      value: event.value,
    })}\n`,
    'utf8',
  );
}
