const c=new AbortController(); c.signal.addEventListener('abort',()=>console.log((c.signal.reason).message)); c.abort(new Error('stop'));
