const value={name:'Ada',age:37};const keys=['age','name']as const;console.log(keys.map(k=>String(value[k])).join('|'));
