const exportsMap=new Set(['.','./testing']);const requested='./internal';if(!exportsMap.has(requested))throw new Error('unsupported package subpath');console.log(requested);
