const values=await Promise.allSettled([Promise.resolve(1)]); if(values[0]?.status==='fulfilled'){const n:number=values[0].value; void n;} export {};
