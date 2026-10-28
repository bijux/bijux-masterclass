const result: Promise<readonly [number, string]> = Promise.all([Promise.resolve(1), Promise.resolve('ok')]);
void result;
