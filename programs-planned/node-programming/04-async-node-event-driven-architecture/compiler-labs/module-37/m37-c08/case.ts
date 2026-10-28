import{AsyncLocalStorage}from'node:async_hooks';const s=new AsyncLocalStorage();if(s.getStore()===undefined)throw new Error('no active context');
