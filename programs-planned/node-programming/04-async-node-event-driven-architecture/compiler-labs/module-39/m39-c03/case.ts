interface R{drain(signal:AbortSignal):Promise<void>;close():Promise<void>}const r:R={drain:async()=>undefined,close:async()=>undefined};void r;export {};
