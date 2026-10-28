export interface EventInput {
  readonly type: string;
  readonly data: unknown;
}

export function encodeEvent(id: number, input: EventInput): Buffer {
  return Buffer.from(
    `id: ${id}\nevent: ${input.type}\ndata: ${JSON.stringify(input.data)}\n\n`,
    'utf8',
  );
}
