export type Replay<T>={kind:'events';values:readonly T[]}|{kind:'gap';oldest:number};
