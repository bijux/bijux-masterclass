function describe(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}
console.log(describe(new Error('bad input')));
