const p: Promise<number> = Promise.resolve(2).then(value => value * 2); void p; export {};
