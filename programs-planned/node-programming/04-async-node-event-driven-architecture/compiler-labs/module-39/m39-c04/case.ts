interface R{drain(signal:AbortSignal):Promise<void>;close():Promise<void>}const r:R={close:async()=>undefined};void r;export {};
