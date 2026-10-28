type Result = { ok: true; value: number } | { ok: false; issues: string[] };
function use(result: Result): number {
  return result.value;
}
console.log(use({ ok: true, value: 1 }));
