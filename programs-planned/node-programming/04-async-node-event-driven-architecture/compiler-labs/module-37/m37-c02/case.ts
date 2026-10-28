import{AsyncLocalStorage}from'node:async_hooks';const s=new AsyncLocalStorage<{runId:string}>();const id:string=s.getStore().runId;void id;export {};
