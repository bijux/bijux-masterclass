import { ServiceProblem } from './errors.js';

export type ServiceEventType =
  | 'job-created'
  | 'job-running'
  | 'job-succeeded'
  | 'job-failed'
  | 'job-cancelled'
  | 'service-quiescing';

export interface ServiceEvent {
  readonly sequence: number;
  readonly type: ServiceEventType;
  readonly occurredAtMs: number;
  readonly jobId?: string;
  readonly revision?: number;
}

type Listener = (event: ServiceEvent) => void;

export class EventJournal {
  readonly #events: ServiceEvent[] = [];
  readonly #listeners = new Map<number, Listener>();
  #nextSequence = 1;
  #nextListener = 1;
  #closed = false;

  constructor(
    readonly maxEvents: number,
    readonly maxSubscribers: number,
  ) {}

  append(input: Omit<ServiceEvent, 'sequence'>): ServiceEvent {
    if (this.#closed) throw new Error('event journal is closed');
    const event: ServiceEvent = { sequence: this.#nextSequence, ...input };
    this.#nextSequence += 1;
    this.#events.push(event);
    while (this.#events.length > this.maxEvents) this.#events.shift();
    for (const listener of this.#listeners.values()) listener(event);
    return event;
  }

  open(after: number | undefined, listener: Listener): {
    readonly replay: readonly ServiceEvent[];
    readonly dispose: () => void;
  } {
    if (this.#closed) throw new Error('event journal is closed');
    if (this.#listeners.size >= this.maxSubscribers) {
      throw new ServiceProblem('OVER_CAPACITY', 503, 'Event subscriber capacity is full');
    }
    const latest = this.latestSequence();
    const oldest = this.#events[0]?.sequence;
    if (after !== undefined) {
      if (!Number.isSafeInteger(after) || after < 0 || after > latest) {
        throw new ServiceProblem('INVALID_REQUEST', 400, 'Invalid event cursor');
      }
      if (oldest !== undefined && after < oldest - 1) {
        throw new ServiceProblem('REPLAY_GAP', 409, `Requested event cursor predates retained history at ${oldest}`);
      }
    }
    const id = this.#nextListener;
    this.#nextListener += 1;
    this.#listeners.set(id, listener);
    let disposed = false;
    return {
      replay: after === undefined ? [] : this.#events.filter((event) => event.sequence > after),
      dispose: () => {
        if (disposed) return;
        disposed = true;
        this.#listeners.delete(id);
      },
    };
  }

  latestSequence(): number {
    return this.#events.at(-1)?.sequence ?? 0;
  }

  subscriberCount(): number {
    return this.#listeners.size;
  }

  close(): void {
    if (this.#closed) return;
    this.#closed = true;
    this.#listeners.clear();
  }
}
