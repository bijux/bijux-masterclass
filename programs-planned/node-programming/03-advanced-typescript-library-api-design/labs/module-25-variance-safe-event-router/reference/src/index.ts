export type Listener<in T>=(value:T)=>void;
export class EventRouter<E extends object>{
  #listeners=new Map<keyof E,Set<Listener<E[keyof E]>>>();
  on<K extends keyof E>(key:K,listener:Listener<E[K]>):()=>void{
    const set=this.#listeners.get(key)??new Set<Listener<E[keyof E]>>();
    set.add(listener as Listener<E[keyof E]>);this.#listeners.set(key,set);
    let active=true;return()=>{if(active){active=false;set.delete(listener as Listener<E[keyof E]>);}};
  }
  emit<K extends keyof E>(key:K,value:E[K]):void{
    const snapshot=[...(this.#listeners.get(key)??[])];
    for(const listener of snapshot)(listener as Listener<E[K]>)(value);
  }
  listenerCount<K extends keyof E>(key:K):number{return this.#listeners.get(key)?.size??0;}
}
