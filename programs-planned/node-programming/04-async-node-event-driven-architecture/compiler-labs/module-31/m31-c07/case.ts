const trace=['sync']; queueMicrotask(()=>{trace.push('microtask'); console.log(trace.join(','));});
