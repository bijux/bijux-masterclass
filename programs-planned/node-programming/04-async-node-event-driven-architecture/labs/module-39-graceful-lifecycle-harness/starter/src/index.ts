export interface Closable { readonly name: string; close(): Promise<void>; }
export async function closeReverse(resources: readonly Closable[]): Promise<void> {
  for (const resource of [...resources].reverse()) await resource.close();
}
