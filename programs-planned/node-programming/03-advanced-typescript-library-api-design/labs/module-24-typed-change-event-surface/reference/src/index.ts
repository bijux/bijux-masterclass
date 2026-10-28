export type StringKey<T>=Extract<keyof T,string>;
export type ChangeEvent<T>={[K in StringKey<T>]:Readonly<{type:`${K}Changed`;key:K;previous:T[K];current:T[K]}>}[StringKey<T>];
export type EventFor<T,K extends StringKey<T>>=Extract<ChangeEvent<T>,{readonly key:K}>;
export class ChangeStore<T extends object>{
  #state:T;#listeners=new Map<string,Set<(event:ChangeEvent<T>)=>void>>();
  constructor(initial:T){this.#state={...initial};}
  snapshot():Readonly<T>{return Object.freeze({...this.#state});}
  on<K extends StringKey<T>>(name:`${K}Changed`,listener:(event:EventFor<T,K>)=>void):()=>void{
    const set=this.#listeners.get(name)??new Set<(event:ChangeEvent<T>)=>void>();
    set.add(listener as (event:ChangeEvent<T>)=>void);this.#listeners.set(name,set);
    return()=>{set.delete(listener as (event:ChangeEvent<T>)=>void);};
  }
  set<K extends StringKey<T>>(key:K,current:T[K]):void{
    const previous=this.#state[key];this.#state={...this.#state,[key]:current};
    const event={type:`${key}Changed`,key,previous,current} as unknown as EventFor<T,K>;
    for(const listener of [...(this.#listeners.get(event.type)??[])])listener(event);
  }
}
