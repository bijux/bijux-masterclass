const supported=new Set(['string','number','object']);const requested='discriminatedUnion';if(!supported.has(requested))throw new Error('extension not implemented');console.log(requested);
