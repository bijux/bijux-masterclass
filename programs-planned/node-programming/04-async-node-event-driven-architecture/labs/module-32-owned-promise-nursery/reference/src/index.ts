export type TaskOutcome<T> =
  | { readonly id: string; readonly index: number; readonly status: 'fulfilled'; readonly value: T }
  | { readonly id: string; readonly index: number; readonly status: 'rejected'; readonly error: unknown };

interface Entry<T> {
  readonly id: string;
  readonly index: number;
  readonly promise: Promise<TaskOutcome<T>>;
}

export class TaskNursery<T> {
  #open = true;
  #entries: Entry<T>[] = [];
  #ids = new Set<string>();
  #joinPromise: Promise<readonly TaskOutcome<T>[]> | undefined;

  get size(): number { return this.#entries.length; }
  get isOpen(): boolean { return this.#open; }

  spawn(id: string, run: () => Promise<T>): number {
    if (!this.#open) throw new Error('nursery is closed');
    if (id.length === 0) throw new Error('task id must not be empty');
    if (this.#ids.has(id)) throw new Error(`duplicate task id: ${id}`);
    const index = this.#entries.length;
    this.#ids.add(id);
    const promise = Promise.resolve()
      .then(run)
      .then<TaskOutcome<T>, TaskOutcome<T>>(
        value => ({ id, index, status: 'fulfilled', value }),
        error => ({ id, index, status: 'rejected', error }),
      );
    this.#entries.push({ id, index, promise });
    return index;
  }

  close(): void { this.#open = false; }

  join(): Promise<readonly TaskOutcome<T>[]> {
    this.close();
    this.#joinPromise ??= Promise.all(this.#entries.map(entry => entry.promise));
    return this.#joinPromise;
  }
}
