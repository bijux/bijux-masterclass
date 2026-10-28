const keys=['name','tags']as const;const value={name:'Ada',tags:['ts']};console.log(keys.map(k=>`${k}=${JSON.stringify(value[k])}`).join(';'));
