function get<T,K extends keyof T>(value:T,key:K):T[K]{return value[key];}const key:string='name';const result=get({name:'Ada'},key);console.log(result);
