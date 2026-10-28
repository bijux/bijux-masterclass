function get<T,K extends keyof T>(value:T,key:K):T[K]{return value[key];}const age=get({name:'Ada',age:37},'age');const n:number=age;console.log(n);
