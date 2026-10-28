type E={type:'start';id:string}|{type:'fail';error:unknown};declare const e:E;if(e.type==='start'){console.log(e.id);}export {};
