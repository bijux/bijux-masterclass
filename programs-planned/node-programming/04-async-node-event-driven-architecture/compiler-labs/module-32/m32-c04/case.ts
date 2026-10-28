const values=await Promise.allSettled([Promise.resolve(1)]); const n:number=values[0]!.value; void n; export {};
