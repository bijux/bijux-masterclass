export interface LifecycleResource {
  readonly name: string;
  start(): Promise<void>;
  quiesce(): Promise<void>;
  drain(signal: AbortSignal): Promise<void>;
  force(): Promise<void>;
  close(): Promise<void>;
}
export type LifecycleState = 'new' | 'starting' | 'ready' | 'quiescing' | 'closed' | 'failed';
export interface LifecycleIssue { readonly resource: string; readonly phase: string; readonly error: unknown; }
export interface ShutdownReport { readonly forced: boolean; readonly issues: readonly LifecycleIssue[]; }

export class LifecycleHost {
  #state: LifecycleState = 'new';
  #started: LifecycleResource[] = [];
  #shutdown: Promise<ShutdownReport> | undefined;
  constructor(private readonly resources: readonly LifecycleResource[]) {}
  get state(): LifecycleState { return this.#state; }

  async start(): Promise<void> {
    if (this.#state !== 'new') throw new Error(`cannot start from ${this.#state}`);
    this.#state = 'starting';
    try {
      for (const resource of this.resources) {
        await resource.start();
        this.#started.push(resource);
      }
      this.#state = 'ready';
    } catch (error) {
      this.#state = 'failed';
      const rollback: unknown[] = [];
      for (const resource of [...this.#started].reverse()) {
        try { await resource.close(); } catch (closeError) { rollback.push(closeError); }
      }
      if (rollback.length > 0) throw new AggregateError([error, ...rollback], 'startup and rollback failed');
      throw error;
    }
  }

  shutdown(graceMilliseconds: number): Promise<ShutdownReport> {
    this.#shutdown ??= this.#shutdownOnce(graceMilliseconds);
    return this.#shutdown;
  }

  async #shutdownOnce(graceMilliseconds: number): Promise<ShutdownReport> {
    if (!Number.isFinite(graceMilliseconds) || graceMilliseconds < 0) throw new RangeError('invalid grace');
    if (this.#state === 'closed') return { forced: false, issues: [] };
    this.#state = 'quiescing';
    const issues: LifecycleIssue[] = [];
    for (const resource of this.#started) {
      try { await resource.quiesce(); } catch (error) { issues.push({ resource: resource.name, phase: 'quiesce', error }); }
    }
    const controller = new AbortController();
    let forced = false;
    let resolveDeadline!: () => void;
    const deadline = new Promise<void>(resolve => { resolveDeadline = resolve; });
    const timer = setTimeout(() => { forced = true; controller.abort(new Error('grace expired')); resolveDeadline(); }, graceMilliseconds);
    const drains = this.#started.map(async resource => {
      try { await resource.drain(controller.signal); }
      catch (error) { issues.push({ resource: resource.name, phase: 'drain', error }); }
    });
    const allDrained = Promise.all(drains).then(() => undefined);
    await Promise.race([allDrained, deadline]);
    if (forced) {
      for (const resource of this.#started) {
        try { await resource.force(); } catch (error) { issues.push({ resource: resource.name, phase: 'force', error }); }
      }
    }
    await allDrained;
    clearTimeout(timer);
    for (const resource of [...this.#started].reverse()) {
      try { await resource.close(); } catch (error) { issues.push({ resource: resource.name, phase: 'close', error }); }
    }
    this.#state = 'closed';
    return { forced, issues };
  }
}
