import { randomUUID } from 'node:crypto';
import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { dirname, basename, join } from 'node:path';
import { ObjectAtlas } from './atlas.js';
import { decodeAtlas, encodeAtlas } from './codec.js';
import { StorageError } from './errors.js';
export interface AtlasStore { load():Promise<ObjectAtlas>; save(atlas:ObjectAtlas):Promise<void> }
export class FileAtlasStore implements AtlasStore {
  constructor(readonly path:string){}
  async load():Promise<ObjectAtlas>{try{return ObjectAtlas.fromSnapshot(decodeAtlas(await readFile(this.path,'utf8')));}catch(error){if(isErrno(error,'ENOENT'))return ObjectAtlas.empty();if(error instanceof Error&&error.name!=='StorageError')throw error;throw new StorageError(`failed to load ${this.path}`,{cause:error});}}
  async save(atlas:ObjectAtlas):Promise<void>{const directory=dirname(this.path),temporary=join(directory,`.${basename(this.path)}.${process.pid}.${randomUUID()}.tmp`);try{await mkdir(directory,{recursive:true});await writeFile(temporary,encodeAtlas(atlas.snapshot()),{encoding:'utf8',flag:'wx'});await rename(temporary,this.path);}catch(error){await rm(temporary,{force:true}).catch(()=>undefined);throw new StorageError(`failed to save ${this.path}`,{cause:error});}}
}
function isErrno(value:unknown,code:string):boolean{return typeof value==='object'&&value!==null&&'code'in value&&(value as {code?:unknown}).code===code;}
