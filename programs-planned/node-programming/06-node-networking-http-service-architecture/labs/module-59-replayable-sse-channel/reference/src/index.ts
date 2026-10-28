import http from 'node:http';

export interface EventInput {
  readonly type: string;
  readonly data: unknown;
}
export interface JournalEvent extends EventInput {
  readonly id: number;
  readonly encoded: Buffer;
}

export class ReplayGapError extends Error {
  constructor(readonly requested: number, readonly oldest: number) {
    super(`event ${requested} is older than retained history beginning at ${oldest}`);
    this.name = 'ReplayGapError';
  }
}

export function encodeEvent(id: number, input: EventInput): Buffer {
  if (!Number.isSafeInteger(id) || id < 1) throw new RangeError('event id');
  if (!/^[A-Za-z0-9_-]{1,64}$/.test(input.type)) throw new Error('invalid event type');
  const data = JSON.stringify(input.data);
  const lines = data.split(/\r?\n/).map((line) => `data: ${line}`).join('\n');
  return Buffer.from(`id: ${id}\nevent: ${input.type}\n${lines}\n\n`, 'utf8');
}

interface Subscriber {
  readonly listener: (event: JournalEvent) => void;
}

export class EventJournal {
  readonly #events: JournalEvent[] = [];
  readonly #subscribers = new Map<number, Subscriber>();
  #nextId = 1;
  #nextSubscriber = 1;
  #closed = false;

  constructor(readonly maxEvents: number, readonly maxSubscribers: number) {
    if (!Number.isInteger(maxEvents) || maxEvents < 1) throw new RangeError('maxEvents');
    if (!Number.isInteger(maxSubscribers) || maxSubscribers < 1) throw new RangeError('maxSubscribers');
  }

  append(input: EventInput): JournalEvent {
    if (this.#closed) throw new Error('journal is closed');
    const id = this.#nextId;
    this.#nextId += 1;
    const event: JournalEvent = { id, ...input, encoded: encodeEvent(id, input) };
    this.#events.push(event);
    while (this.#events.length > this.maxEvents) this.#events.shift();
    for (const subscriber of this.#subscribers.values()) subscriber.listener(event);
    return event;
  }

  open(after: number | undefined, listener: (event: JournalEvent) => void): {
    readonly replay: readonly JournalEvent[];
    readonly dispose: () => void;
  } {
    if (this.#closed) throw new Error('journal is closed');
    if (this.#subscribers.size >= this.maxSubscribers) throw new Error('subscriber capacity');
    const oldest = this.#events[0]?.id;
    const latest = this.#events.at(-1)?.id ?? 0;
    if (after !== undefined) {
      if (!Number.isSafeInteger(after) || after < 0) throw new Error('invalid cursor');
      if (after > latest) throw new Error('cursor is ahead of journal');
      if (oldest !== undefined && after < oldest - 1) throw new ReplayGapError(after, oldest);
    }
    const id = this.#nextSubscriber;
    this.#nextSubscriber += 1;
    this.#subscribers.set(id, { listener });
    const replay = this.#events.filter((event) => after === undefined ? false : event.id > after);
    let disposed = false;
    return {
      replay,
      dispose: () => {
        if (disposed) return;
        disposed = true;
        this.#subscribers.delete(id);
      },
    };
  }

  latestId(): number { return this.#events.at(-1)?.id ?? 0; }
  subscriberCount(): number { return this.#subscribers.size; }
  close(): void { this.#closed = true; this.#subscribers.clear(); }
}

export async function startSseServer(options: {
  readonly journal: EventJournal;
  readonly heartbeatMs: number;
  readonly maxSubscriberQueueBytes: number;
}): Promise<{ readonly url: string; close(): Promise<void> }> {
  const responses = new Set<http.ServerResponse>();
  const server = http.createServer((request, response) => {
    const url = new URL(request.url ?? '/', 'http://sse.invalid');
    if (request.method !== 'GET' || url.pathname !== '/events') {
      response.writeHead(404, { 'content-length': '0' });
      response.end();
      return;
    }
    const afterText = url.searchParams.get('after');
    const after = afterText === null ? undefined : Number(afterText);
    let subscription: ReturnType<EventJournal['open']>;
    const queue: Buffer[] = [];
    let queuedBytes = 0;
    let pressured = false;
    let closed = false;

    const cleanup = () => {
      if (closed) return;
      closed = true;
      clearInterval(heartbeat);
      subscription.dispose();
      responses.delete(response);
      queue.length = 0;
      queuedBytes = 0;
    };

    const flush = () => {
      if (closed || pressured) return;
      while (queue.length > 0) {
        const bytes = queue.shift();
        if (!bytes) break;
        queuedBytes -= bytes.byteLength;
        if (!response.write(bytes)) {
          pressured = true;
          response.once('drain', () => { pressured = false; flush(); });
          break;
        }
      }
    };

    const enqueue = (bytes: Buffer) => {
      if (closed) return;
      if (queuedBytes + bytes.byteLength > options.maxSubscriberQueueBytes) {
        cleanup();
        response.destroy(new Error('slow subscriber'));
        return;
      }
      queue.push(bytes);
      queuedBytes += bytes.byteLength;
      flush();
    };

    try {
      subscription = options.journal.open(after, (event) => enqueue(event.encoded));
    } catch (error) {
      const body = Buffer.from(JSON.stringify({ code: error instanceof ReplayGapError ? 'REPLAY_GAP' : 'INVALID_CURSOR' }));
      response.writeHead(error instanceof ReplayGapError ? 409 : 400, {
        'content-type': 'application/problem+json',
        'content-length': String(body.byteLength),
      });
      response.end(body);
      return;
    }

    response.writeHead(200, {
      'content-type': 'text/event-stream; charset=utf-8',
      'cache-control': 'no-cache',
      connection: 'keep-alive',
    });
    responses.add(response);
    for (const event of subscription.replay) enqueue(event.encoded);
    const heartbeat = setInterval(() => enqueue(Buffer.from(': heartbeat\n\n')), options.heartbeatMs);
    response.once('close', cleanup);
    response.once('error', cleanup);
  });

  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  if (address === null || typeof address === 'string') throw new Error('address');
  return {
    url: `http://127.0.0.1:${address.port}/events`,
    close: async () => {
      for (const response of responses) response.end();
      await new Promise<void>((resolve) => server.close(() => resolve()));
    },
  };
}
