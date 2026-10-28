async function load(): Promise<string> {
  throw new Error('read failed');
}
void load().catch((error: unknown) => console.error(error instanceof Error ? error.message : String(error)));
