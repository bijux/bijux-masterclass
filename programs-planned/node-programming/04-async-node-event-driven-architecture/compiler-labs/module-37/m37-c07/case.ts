import{AsyncLocalStorage}from'node:async_hooks';const s=new AsyncLocalStorage();await s.run('run',async()=>{await Promise.resolve();console.log(s.getStore());});
