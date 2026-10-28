export function parseCursor(text:string|undefined): number|undefined { if(text===undefined)return undefined; const value=Number(text); return Number.isSafeInteger(value)&&value>=0?value:undefined; }
