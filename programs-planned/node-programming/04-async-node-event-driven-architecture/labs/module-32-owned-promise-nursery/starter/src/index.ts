export type Settlement<T> =
  | { readonly status: 'fulfilled'; readonly value: T }
  | { readonly status: 'rejected'; readonly error: unknown };

export async function settleOne<T>(run: () => Promise<T>): Promise<Settlement<T>> {
  try {
    return { status: 'fulfilled', value: await run() };
  } catch (error) {
    return { status: 'rejected', error };
  }
}
