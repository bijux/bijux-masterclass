export interface CounterRecord { readonly name:string; readonly balance:number }
export function validateBalance(value:unknown):number { if(typeof value!=='number'||!Number.isSafeInteger(value)||value<0) throw new Error('balance must be a non-negative safe integer'); return value; }
export function normalizeName(raw:string):string { const name=raw.trim(); if(name==='') throw new Error('name must not be empty'); return name; }

export class CounterBank {
  readonly #balances: Map<string,number>;
  private constructor(records:readonly CounterRecord[]){ this.#balances=new Map(records.map((r)=>[r.name,r.balance])); }
  static create(records:readonly CounterRecord[]):CounterBank { const seen=new Set<string>(); const clean=records.map((r)=>{const name=normalizeName(r.name);if(seen.has(name))throw new Error(`duplicate counter: ${name}`);seen.add(name);return {name,balance:validateBalance(r.balance)};}); return new CounterBank(clean); }
  static fromSnapshot(input:unknown):CounterBank { if(!Array.isArray(input))throw new Error('snapshot must be an array'); const records=input.map((value,index)=>{if(typeof value!=='object'||value===null)throw new Error(`record ${index} must be an object`);const r=value as Record<string,unknown>;if(typeof r.name!=='string')throw new Error(`record ${index}.name must be a string`);return {name:r.name,balance:validateBalance(r.balance)};}); return CounterBank.create(records); }
  static isCounterBank(value:unknown):value is CounterBank { return typeof value==='object'&&value!==null&&#balances in value; }
  balance(name:string):number { const key=normalizeName(name); const value=this.#balances.get(key); if(value===undefined)throw new Error(`unknown counter: ${key}`); return value; }
  transfer(fromRaw:string,toRaw:string,amountRaw:number):void { const from=normalizeName(fromRaw),to=normalizeName(toRaw),amount=validateBalance(amountRaw); if(from===to)throw new Error('source and destination must differ'); const a=this.balance(from),b=this.balance(to); if(a<amount)throw new Error('insufficient balance'); const nextB=b+amount; if(!Number.isSafeInteger(nextB))throw new Error('destination balance overflow'); this.#balances.set(from,a-amount); this.#balances.set(to,nextB); }
  snapshot():readonly CounterRecord[]{ return Object.freeze([...this.#balances].sort(([a],[b])=>a.localeCompare(b)).map(([name,balance])=>Object.freeze({name,balance}))); }
}
