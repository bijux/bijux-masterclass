const c=new AbortController(); c.abort(new Error('x')); const reason:unknown=c.signal.reason; void reason; export {};
