import { inspect } from 'node:util';
export function validateMillimetres(value:unknown):number { if(typeof value!=='number'||!Number.isSafeInteger(value)||value<0)throw new Error('millimetres must be a non-negative safe integer'); return value; }
export interface DistanceRecord { readonly format:'DISTANCE_V1';readonly millimetres:number }
export class Distance implements Iterable<readonly [unit:string,value:number]> {
  readonly #millimetres:number;
  constructor(value:number){this.#millimetres=validateMillimetres(value);}
  static metres(value:number):Distance { if(!Number.isFinite(value)||value<0)throw new Error('metres must be finite and non-negative'); const mm=value*1000;if(!Number.isSafeInteger(mm))throw new Error('metres must resolve to whole safe millimetres');return new Distance(mm); }
  get millimetres():number{return this.#millimetres;}
  equals(other:Distance):boolean{return this.#millimetres===other.#millimetres;}
  [Symbol.toPrimitive](hint:string):string|number { return hint==='number'?this.#millimetres:`${(this.#millimetres/1000).toFixed(3)} m`; }
  get [Symbol.toStringTag]():string{return'Distance';}
  *[Symbol.iterator]():Iterator<readonly [string,number]>{yield ['metres',Math.trunc(this.#millimetres/1000)] as const;yield ['millimetres',this.#millimetres%1000] as const;}
  toJSON():DistanceRecord{return{format:'DISTANCE_V1',millimetres:this.#millimetres};}
  [inspect.custom]():string{return`Distance { millimetres: ${this.#millimetres} }`;}
}
