export type JsonAtom=string|number|boolean|null;
export type DraftState='open'|'committed'|'rolled-back';
export interface DraftSession { readonly draft:Record<string,JsonAtom>; readonly state:DraftState; commit():Readonly<Record<string,JsonAtom>>; rollback():void; [Symbol.dispose]():void }
export function validateKey(raw:PropertyKey):string{if(typeof raw!=='string'||raw===''||raw==='__proto__'||raw==='prototype'||raw==='constructor')throw new Error('invalid draft key');return raw;}
export function copyRecord(source:Readonly<Record<string,JsonAtom>>):Record<string,JsonAtom>{return Object.assign(Object.create(null),source) as Record<string,JsonAtom>;}
export function openDraft(source:Readonly<Record<string,JsonAtom>>,validate:(key:string,value:JsonAtom)=>void):DraftSession{
  const target=copyRecord(source);let state:DraftState='open';
  const ensure=()=>{if(state!=='open')throw new Error(`draft is ${state}`);};
  const revocable=Proxy.revocable(target,{
    set(t,key,value,receiver){ensure();const k=validateKey(key);if(value!==null&&typeof value!=='string'&&typeof value!=='number'&&typeof value!=='boolean')throw new Error(`unsupported value: ${k}`);validate(k,value);return Reflect.set(t,k,value,receiver);},
    deleteProperty(t,key){ensure();const k=validateKey(key);return Reflect.deleteProperty(t,k);},
    defineProperty(t,key,descriptor){ensure();const k=validateKey(key);if(!('value'in descriptor)||descriptor.get!==undefined||descriptor.set!==undefined)throw new Error(`draft properties must be data: ${k}`);const value=descriptor.value;if(value!==null&&typeof value!=='string'&&typeof value!=='number'&&typeof value!=='boolean')throw new Error(`unsupported value: ${k}`);validate(k,value);return Reflect.defineProperty(t,k,{value,writable:true,enumerable:true,configurable:true});}
  });
  return {get draft(){return revocable.proxy;},get state(){return state;},commit(){ensure();for(const [k,v] of Object.entries(target))validate(k,v);state='committed';const result=Object.freeze({...target});revocable.revoke();return result;},rollback(){ensure();state='rolled-back';revocable.revoke();},[Symbol.dispose](){if(state==='open'){state='rolled-back';revocable.revoke();}}};
}
