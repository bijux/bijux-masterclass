interface E{started:readonly [string]} function emit<K extends keyof E>(k:K,...a:E[K]){void k;void a;} emit('started',1); export {};
