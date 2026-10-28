export type Command<Args extends readonly unknown[], Result> = (...args: Args) => Result;
export function adaptMethod<This, Args extends readonly unknown[], Result>(receiver: This, method: (this: This, ...args: Args) => Result): Command<Args,Result> {
  return (...args: Args): Result => Reflect.apply(method,receiver,args) as Result;
}
export function constructWith<Args extends readonly unknown[], Instance>(ctor: new (...args: Args)=>Instance, args: Args): Instance { return Reflect.construct(ctor,args) as Instance; }

export class CommandRegistry {
  readonly #commands=new Map<string,Command<readonly unknown[],unknown>>();
  register<Args extends readonly unknown[],Result>(name:string, command:Command<Args,Result>):void {
    const key=name.trim(); if(key==='') throw new Error('command name must not be empty'); if(this.#commands.has(key)) throw new Error(`duplicate command: ${key}`);
    this.#commands.set(key,command as Command<readonly unknown[],unknown>);
  }
  invoke<Result>(name:string,...args:readonly unknown[]):Result { const c=this.#commands.get(name); if(c===undefined) throw new Error(`unknown command: ${name}`); return c(...args) as Result; }
  names():readonly string[]{return [...this.#commands.keys()].sort();}
}
