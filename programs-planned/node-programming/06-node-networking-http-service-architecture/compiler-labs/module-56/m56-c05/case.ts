export type Attempt = {kind:'response';status:number}|{kind:'transport';code:string}|{kind:'deadline'};
