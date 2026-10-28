const timer=setTimeout(()=>undefined,1); timer.unref(); clearTimeout(timer); export {};
