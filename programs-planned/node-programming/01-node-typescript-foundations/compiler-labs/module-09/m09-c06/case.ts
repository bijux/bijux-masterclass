async function work(signal: AbortSignal): Promise<string> {
  if (signal.aborted) throw signal.reason ?? new Error('aborted');
  return 'done';
}
console.log(await work(new AbortController().signal));
