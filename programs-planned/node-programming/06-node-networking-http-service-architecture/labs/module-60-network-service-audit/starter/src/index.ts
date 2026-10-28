export type HealthView =
  | { readonly health: 'healthy'; readonly readiness: 'ready' }
  | { readonly health: 'healthy'; readonly readiness: 'not-ready' };

export class AuditService {
  #ready = false;

  markReady(): void {
    this.#ready = true;
  }

  quiesce(): void {
    this.#ready = false;
  }

  health(): HealthView {
    return this.#ready
      ? { health: 'healthy', readiness: 'ready' }
      : { health: 'healthy', readiness: 'not-ready' };
  }
}
