const value={name:'Ada'} as Record<string,string>;const key='role';const selected=value[key];if(selected===undefined)throw new Error('missing dynamic key');console.log(selected);
