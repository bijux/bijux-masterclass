export interface RecordItem{readonly id:string;readonly score:number}export function total(items:readonly RecordItem[]):number{return items.reduce((sum,item)=>sum+item.score,0);}
