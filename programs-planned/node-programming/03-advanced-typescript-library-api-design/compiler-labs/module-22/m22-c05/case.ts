function choose<T>(value:T|undefined,fallback:NoInfer<T>):T{return value??fallback;}const selected=choose<'on'|'off'>('on','off');console.log(selected);
