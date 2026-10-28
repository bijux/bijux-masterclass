export interface OwnedResource {
  readonly name: string;
  close(): Promise<void>;
}

export type ResourceFactory = (name: string) => Promise<OwnedResource>;

export interface TerminalReport {
  readonly startedResources: number;
  readonly closedResources: number;
  readonly acceptedJobs: number;
  readonly succeededJobs: number;
  readonly cancelledJobs: number;
  readonly openedSubscribers: number;
  readonly closedSubscribers: number;
}

type Job = {
  readonly id: number;
  state: 'queued' | 'running' | 'succeeded' | 'cancelled';
  readonly workMs: number;
};

export class AuditService {
  readonly #resources: OwnedResource[] = [];
  readonly #jobs = new Map<number, Job>();
  readonly #subscribers = new Set<number>();
  readonly #timers = new Map<number, ReturnType<typeof setTimeout>>();
  #nextJob = 1;
  #nextSubscriber = 1;
  #state: 'starting' | 'ready' | 'quiescing' | 'stopped' = 'starting';
  #closePromise: Promise<TerminalReport> | undefined;
  #closedResources = 0;
  #closedSubscribers = 0;

  private constructor(
    readonly maxJobs: number,
    readonly maxActive: number,
  ) {}

  static async start(options: {
    readonly maxJobs: number;
    readonly maxActive: number;
    readonly resourceNames: readonly string[];
    readonly createResource: ResourceFactory;
  }): Promise<AuditService> {
    const service = new AuditService(options.maxJobs, options.maxActive);
    try {
      for (const name of options.resourceNames) {
        service.#resources.push(await options.createResource(name));
      }
      service.#state = 'ready';
      return service;
    } catch (error) {
      for (const resource of [...service.#resources].reverse()) {
        try {
          await resource.close();
          service.#closedResources += 1;
        } catch {
          // Continue rollback so every acquired resource is observed.
        }
      }
      service.#state = 'stopped';
      throw error;
    }
  }

  health(): { readonly health: 'healthy'; readonly readiness: 'ready' | 'not-ready'; readonly state: string } {
    return {
      health: 'healthy',
      readiness: this.#state === 'ready' ? 'ready' : 'not-ready',
      state: this.#state,
    };
  }

  submit(workMs: number): number {
    if (this.#state !== 'ready') throw new Error('NOT_READY');
    if (this.#jobs.size >= this.maxJobs) throw new Error('OVER_CAPACITY');
    const id = this.#nextJob;
    this.#nextJob += 1;
    this.#jobs.set(id, { id, state: 'queued', workMs });
    this.pump();
    return id;
  }

  subscribe(): { readonly id: number; dispose(): void } {
    if (this.#state === 'stopped') throw new Error('STOPPED');
    const id = this.#nextSubscriber;
    this.#nextSubscriber += 1;
    this.#subscribers.add(id);
    let disposed = false;
    return {
      id,
      dispose: () => {
        if (disposed) return;
        disposed = true;
        if (this.#subscribers.delete(id)) this.#closedSubscribers += 1;
      },
    };
  }

  private pump(): void {
    const active = [...this.#jobs.values()].filter((job) => job.state === 'running').length;
    let available = this.maxActive - active;
    for (const job of this.#jobs.values()) {
      if (available <= 0) break;
      if (job.state !== 'queued') continue;
      job.state = 'running';
      available -= 1;
      const timer = setTimeout(() => {
        this.#timers.delete(job.id);
        if (job.state === 'running') job.state = 'succeeded';
        this.pump();
      }, job.workMs);
      this.#timers.set(job.id, timer);
    }
  }

  close(graceMs: number): Promise<TerminalReport> {
    if (this.#closePromise) return this.#closePromise;
    this.#closePromise = this.closeOwned(graceMs);
    return this.#closePromise;
  }

  private async closeOwned(graceMs: number): Promise<TerminalReport> {
    this.#state = 'quiescing';
    for (const id of [...this.#subscribers]) {
      this.#subscribers.delete(id);
      this.#closedSubscribers += 1;
    }
    const deadline = Date.now() + graceMs;
    while ([...this.#jobs.values()].some((job) => job.state === 'queued' || job.state === 'running') && Date.now() < deadline) {
      await new Promise((resolve) => setTimeout(resolve, 2));
    }
    for (const job of this.#jobs.values()) {
      if (job.state === 'queued' || job.state === 'running') {
        const timer = this.#timers.get(job.id);
        if (timer) clearTimeout(timer);
        this.#timers.delete(job.id);
        job.state = 'cancelled';
      }
    }
    for (const resource of [...this.#resources].reverse()) {
      try {
        await resource.close();
      } finally {
        this.#closedResources += 1;
      }
    }
    this.#state = 'stopped';
    const jobs = [...this.#jobs.values()];
    return {
      startedResources: this.#resources.length,
      closedResources: this.#closedResources,
      acceptedJobs: jobs.length,
      succeededJobs: jobs.filter((job) => job.state === 'succeeded').length,
      cancelledJobs: jobs.filter((job) => job.state === 'cancelled').length,
      openedSubscribers: this.#nextSubscriber - 1,
      closedSubscribers: this.#closedSubscribers,
    };
  }
}
