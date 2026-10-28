export interface DocumentRecord { readonly id:string; readonly title:string; readonly text:string; readonly tags:readonly string[]; readonly version:number }
export interface Store { load(id:string):Promise<DocumentRecord>; save(record:DocumentRecord):Promise<void> }
export interface Renderer { render(record:DocumentRecord):string }
export interface Clock { now():string }
export function normalizeTag(raw:string):string { const t=raw.trim().toLowerCase(); if(t==='')throw new Error('tag must not be empty'); return t; }
