export function normalizeName(value:string):string{const result=value.trim().replace(/\s+/g,' ');if(result==='')throw new Error('name must not be empty');return result;}
