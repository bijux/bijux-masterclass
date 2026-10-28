export interface UserV1{readonly format:'USER_V1';readonly id:string;readonly name:string}
export interface UserV2{readonly format:'USER_V2';readonly id:string;readonly displayName:string;readonly tags:readonly string[]}
export type UserResponse=UserV1|UserV2;
export function migrateUser(value:UserResponse):UserV2{return value.format==='USER_V2'?value:Object.freeze({format:'USER_V2',id:value.id,displayName:value.name,tags:Object.freeze([])});}
export function parseUser(input:unknown):UserResponse{if(typeof input!=='object'||input===null)throw new Error('expected object');const format=Reflect.get(input,'format');const id=Reflect.get(input,'id');if(typeof id!=='string'||id==='')throw new Error('invalid id');if(format==='USER_V1'){const name=Reflect.get(input,'name');if(typeof name!=='string')throw new Error('invalid V1 name');return{format,id,name};}if(format==='USER_V2'){const displayName=Reflect.get(input,'displayName');const tags=Reflect.get(input,'tags');if(typeof displayName!=='string'||!Array.isArray(tags)||!tags.every(tag=>typeof tag==='string'))throw new Error('invalid V2');return{format,id,displayName,tags:Object.freeze([...tags])};}throw new Error('unsupported user format');}
/** @deprecated Use `migrateUser(value).displayName`. */
export function displayName(value:UserResponse):string{return value.format==='USER_V1'?value.name:value.displayName;}
