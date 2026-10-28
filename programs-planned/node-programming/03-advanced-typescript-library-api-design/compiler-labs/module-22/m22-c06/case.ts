function choose<T>(value:T|undefined,fallback:NoInfer<T>):T{return value??fallback;}const selected=choose<'on'|'off'>('on','other');console.log(selected);
