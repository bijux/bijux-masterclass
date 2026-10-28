import{AsyncLocalStorage}from'node:async_hooks';const s=new AsyncLocalStorage<{runId:string}>();s.run({runId:'r'},()=>s.getStore()?.runId);export {};
