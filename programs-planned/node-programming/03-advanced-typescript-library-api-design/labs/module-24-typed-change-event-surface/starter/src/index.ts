export interface Profile{readonly name:string;readonly active:boolean}
export function eventName(key:keyof Profile):string{return`${String(key)}Changed`;}
