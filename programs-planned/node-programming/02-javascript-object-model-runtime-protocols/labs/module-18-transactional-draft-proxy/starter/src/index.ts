export type JsonAtom=string|number|boolean|null;
export function validateKey(raw:PropertyKey):string{if(typeof raw!=='string'||raw===''||raw==='__proto__'||raw==='prototype'||raw==='constructor')throw new Error('invalid draft key');return raw;}
export function copyRecord(source:Readonly<Record<string,JsonAtom>>):Record<string,JsonAtom>{return Object.assign(Object.create(null),source) as Record<string,JsonAtom>;}
