const c=new AbortController(); c.abort(new Error('cancelled')); c.signal.throwIfAborted();
