export interface DocumentRecord { readonly id:string; readonly title:string; readonly text:string; readonly tags:readonly string[]; readonly version:number; readonly committedAt?:string }
export interface Store { load(id:string):Promise<DocumentRecord>; save(record:DocumentRecord):Promise<void> }
export interface Renderer { render(record:Readonly<DocumentRecord>):string }
export interface Clock { now():string }
export function normalizeTag(raw:string):string { const t=raw.trim().toLowerCase(); if(t==='')throw new Error('tag must not be empty'); return t; }
function snapshot(record:DocumentRecord):DocumentRecord { return Object.freeze({...record,tags:Object.freeze([...record.tags])}); }
export function addTag(record:DocumentRecord,raw:string):DocumentRecord { const tag=normalizeTag(raw); const tags=[...new Set([...record.tags.map(normalizeTag),tag])].sort(); return snapshot({...record,tags}); }

export function createDocumentApplication(deps:{readonly store:Store;readonly renderer:Renderer;readonly clock:Clock}) {
  return Object.freeze({
    async tagAndCommit(id:string,tag:string):Promise<string>{ const loaded=snapshot(await deps.store.load(id)); const tagged=addTag(loaded,tag); const candidate=snapshot({...tagged,version:tagged.version+1,committedAt:deps.clock.now()}); await deps.store.save(candidate); return deps.renderer.render(candidate); },
    async render(id:string):Promise<string>{ return deps.renderer.render(snapshot(await deps.store.load(id))); },
  });
}
