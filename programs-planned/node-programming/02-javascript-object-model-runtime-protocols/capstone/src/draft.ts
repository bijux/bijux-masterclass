import { DraftClosedError, ValidationError } from './errors.js';
import { cloneAttributes, cloneJson, validateAttributeKey } from './node.js';
import type { JsonValue } from './types.js';
export type DraftState='open'|'committed'|'rolled-back';
export class AttributeDraft implements Disposable {
  readonly #revocable:{readonly proxy:Record<string,JsonValue>;readonly revoke:()=>void}; #state:DraftState='open'; readonly #publish:(candidate:Readonly<Record<string,JsonValue>>)=>void;
  constructor(source:Readonly<Record<string,JsonValue>>,publish:(candidate:Readonly<Record<string,JsonValue>>)=>void){const target=Object.assign(Object.create(null),cloneAttributes(source)) as Record<string,JsonValue>;this.#publish=publish;this.#revocable=Proxy.revocable(target,{set:(t,key,value,receiver)=>{this.#ensure();const k=validateAttributeKey(typeof key==='string'?key:'');const safe=cloneJson(value as JsonValue);return Reflect.set(t,k,safe,receiver);},deleteProperty:(t,key)=>{this.#ensure();const k=validateAttributeKey(typeof key==='string'?key:'');return Reflect.deleteProperty(t,k);},defineProperty:(t,key,d)=>{this.#ensure();const k=validateAttributeKey(typeof key==='string'?key:'');if(!('value'in d)||d.get!==undefined||d.set!==undefined)throw new ValidationError(`draft property must be data: ${k}`);return Reflect.defineProperty(t,k,{value:cloneJson(d.value as JsonValue),writable:true,enumerable:true,configurable:true});}});}
  get draft():Record<string,JsonValue>{this.#ensure();return this.#revocable.proxy;}
  get state():DraftState{return this.#state;}
  commit():void{this.#ensure();const candidate=cloneAttributes(this.#revocable.proxy);this.#publish(candidate);this.#state='committed';this.#revocable.revoke();}
  rollback():void{this.#ensure();this.#state='rolled-back';this.#revocable.revoke();}
  [Symbol.dispose]():void{if(this.#state==='open'){this.#state='rolled-back';this.#revocable.revoke();}}
  #ensure():void{if(this.#state!=='open')throw new DraftClosedError(this.#state);}
}
