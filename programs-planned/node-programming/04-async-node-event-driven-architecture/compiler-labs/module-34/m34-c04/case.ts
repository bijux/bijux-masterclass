interface E{started:readonly [string]} function on<K extends keyof E>(k:K){void k;} on('finished'); export {};
