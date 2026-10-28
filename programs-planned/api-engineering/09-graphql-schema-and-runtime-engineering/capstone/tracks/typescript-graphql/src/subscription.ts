/** Resume validation for an ordered subscription event stream. */

import { ValidationError } from "./model.js";

export interface SubscriptionEvent<
  T = Readonly<Record<string, unknown>>,
> {
  sequence: number;
  payload: T;
}

export class ResumableSubscription {
  constructor(private readonly maximumBuffer = 100) {
    if (maximumBuffer < 1) {
      throw new Error("maximumBuffer must be positive");
    }
  }

  resume<T>(
    events: readonly SubscriptionEvent<T>[],
    after: number,
  ): readonly SubscriptionEvent<T>[] {
    const ordered = [...events].sort(
      (left, right) => left.sequence - right.sequence,
    );
    const delivered: SubscriptionEvent<T>[] = [];
    const seen = new Set<number>();
    let expected = after + 1;

    for (const event of ordered) {
      if (event.sequence <= after || seen.has(event.sequence)) {
        continue;
      }
      if (event.sequence !== expected) {
        throw new ValidationError(
          `subscription gap: expected ${expected}, ` +
            `got ${event.sequence}`,
        );
      }

      delivered.push(event);
      seen.add(event.sequence);
      expected += 1;

      if (delivered.length > this.maximumBuffer) {
        throw new ValidationError(
          "subscription buffer exceeded",
        );
      }
    }

    return delivered;
  }
}
