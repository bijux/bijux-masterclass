export interface CounterRecord { readonly name:string; readonly balance:number }
export function validateBalance(value:unknown):number { if(typeof value!=='number'||!Number.isSafeInteger(value)||value<0) throw new Error('balance must be a non-negative safe integer'); return value; }
export function normalizeName(raw:string):string { const name=raw.trim(); if(name==='') throw new Error('name must not be empty'); return name; }
