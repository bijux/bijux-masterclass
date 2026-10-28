/** Request-scoped batching primitive used by the semantic gateway. */

export class LoadToken<V> {
  value: V | undefined;
  ready = false;

  get(): V | undefined {
    if (!this.ready) {
      throw new Error("loader has not been dispatched");
    }
    return this.value;
  }
}

export class BatchLoader<K, V> {
  private readonly tokens = new Map<K, LoadToken<V>>();
  dispatches = 0;

  constructor(
    private readonly batch: (
      keys: readonly K[],
    ) => ReadonlyMap<K, V>,
  ) {}

  load(key: K): LoadToken<V> {
    let token = this.tokens.get(key);
    if (!token) {
      token = new LoadToken<V>();
      this.tokens.set(key, token);
    }
    return token;
  }

  dispatch(): void {
    const pending = [...this.tokens.entries()]
      .filter(([, token]) => !token.ready)
      .map(([key]) => key);

    if (pending.length === 0) {
      return;
    }

    const values = this.batch(pending);
    this.dispatches += 1;

    for (const key of pending) {
      const token = this.tokens.get(key)!;
      token.value = values.get(key);
      token.ready = true;
    }
  }

  get keyCount(): number {
    return this.tokens.size;
  }
}
