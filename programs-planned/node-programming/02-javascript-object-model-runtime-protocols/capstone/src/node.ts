import type { InspectOptionsStylized } from 'node:util';
import { ValidationError } from './errors.js';
import { ATLAS_INSPECT, NODE_INTERNAL, RUNTIME_META } from './protocols.js';
import type { JsonValue, NodeKind, NodeRecord, NodeView } from './types.js';

const ID = /^[A-Za-z][A-Za-z0-9._-]{0,63}$/u;
const ATTRIBUTE = /^[A-Za-z][A-Za-z0-9._-]{0,63}$/u;
const LIMITS = Object.freeze({ label: 160, attributes: 64, depth: 8, array: 128, object: 128 });

interface KindPolicy { readonly mayHaveChildren: boolean; readonly displayKind: string }
const BASE_POLICY = Object.freeze({ mayHaveChildren: false, displayKind: 'Component' });
function derivedPolicy(values: Partial<KindPolicy>): KindPolicy {
  const descriptors: PropertyDescriptorMap = {};
  for (const [key, value] of Object.entries(values)) descriptors[key] = { value, writable: false, enumerable: true, configurable: false };
  return Object.freeze(Object.create(BASE_POLICY, descriptors) as KindPolicy);
}
const FOLDER_POLICY = derivedPolicy({ mayHaveChildren: true, displayKind: 'Folder' });
const COMPONENT_POLICY = derivedPolicy({ displayKind: 'Component' });
const SERVICE_POLICY = derivedPolicy({ displayKind: 'Service' });

export function policyFor(kind: NodeKind): KindPolicy {
  switch (kind) { case 'folder': return FOLDER_POLICY; case 'component': return COMPONENT_POLICY; case 'service': return SERVICE_POLICY; }
}

export function validateId(raw: string): string { const value = raw.trim(); if (!ID.test(value)) throw new ValidationError(`invalid node id: ${raw}`); return value; }
export function validateKind(value: unknown): NodeKind { if (value !== 'folder' && value !== 'component' && value !== 'service') throw new ValidationError(`invalid node kind: ${String(value)}`); return value; }
export function validateLabel(raw: string): string { const value = raw.trim(); if (value === '' || value.length > LIMITS.label) throw new ValidationError('label must contain 1..160 code units'); return value; }
export function validateAttributeKey(raw: string): string { const value=raw.trim(); if(!ATTRIBUTE.test(value)||value==='__proto__'||value==='prototype'||value==='constructor')throw new ValidationError(`invalid attribute key: ${raw}`); return value; }

export function cloneJson(value: JsonValue, depth=0): JsonValue {
  if (depth > LIMITS.depth) throw new ValidationError('attribute value exceeds maximum nesting depth');
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number') { if (!Number.isFinite(value)) throw new ValidationError('attribute numbers must be finite'); return value; }
  if (Array.isArray(value)) { if(value.length>LIMITS.array)throw new ValidationError('attribute array is too large'); return Object.freeze(value.map((item)=>cloneJson(item,depth+1))); }
  if (typeof value === 'object') {
    const keys=Object.keys(value); if(keys.length>LIMITS.object)throw new ValidationError('attribute object is too large');
    const out=Object.create(null) as Record<string,JsonValue>;
    for(const rawKey of keys){const key=validateAttributeKey(rawKey);out[key]=cloneJson((value as Record<string,JsonValue>)[rawKey]!,depth+1);}
    return Object.freeze(out);
  }
  throw new ValidationError('unsupported attribute value');
}

export function cloneAttributes(value: Readonly<Record<string,JsonValue>>): Readonly<Record<string,JsonValue>> {
  const keys=Object.keys(value); if(keys.length>LIMITS.attributes)throw new ValidationError('too many attributes');
  const out=Object.create(null) as Record<string,JsonValue>; for(const rawKey of keys){const key=validateAttributeKey(rawKey);out[key]=cloneJson(value[rawKey]!);} return Object.freeze(out);
}

interface RuntimeMeta { readonly createdAtRevision: number }
interface InternalPatch { readonly parentId?: string|null; readonly children?: readonly string[]; readonly label?: string; readonly attributes?: Readonly<Record<string,JsonValue>> }

export class AtlasNode {
  declare readonly id: string;
  readonly #kind: NodeKind;
  #label: string;
  #parentId: string|null;
  #children: readonly string[];
  #attributes: Readonly<Record<string,JsonValue>>;
  constructor(record: NodeRecord, createdAtRevision=0) {
    const id=validateId(record.id); this.#kind=validateKind(record.kind); this.#label=validateLabel(record.label); this.#parentId=record.parentId===null?null:validateId(record.parentId); this.#children=Object.freeze(record.children.map(validateId)); this.#attributes=cloneAttributes(record.attributes);
    Object.defineProperty(this,'id',{value:id,writable:false,enumerable:true,configurable:false});
    Object.defineProperty(this,RUNTIME_META,{value:Object.freeze({createdAtRevision}) satisfies RuntimeMeta,writable:false,enumerable:false,configurable:false});
  }
  static isAtlasNode(value:unknown):value is AtlasNode{return typeof value==='object'&&value!==null&&#kind in value;}
  get kind():NodeKind{return this.#kind;} get label():string{return this.#label;} get parentId():string|null{return this.#parentId;} get children():readonly string[]{return Object.freeze([...this.#children]);} get attributes():Readonly<Record<string,JsonValue>>{return cloneAttributes(this.#attributes);} get policy():KindPolicy{return policyFor(this.#kind);}
  toRecord():NodeRecord{return Object.freeze({id:this.id,kind:this.#kind,label:this.#label,parentId:this.#parentId,children:Object.freeze([...this.#children]),attributes:cloneAttributes(this.#attributes)});}
  toView():NodeView{return Object.freeze({...this.toRecord(),childCount:this.#children.length,policy:this.policy});}
  [NODE_INTERNAL](patch:InternalPatch):void{if(patch.parentId!==undefined)this.#parentId=patch.parentId===null?null:validateId(patch.parentId);if(patch.children!==undefined)this.#children=Object.freeze(patch.children.map(validateId));if(patch.label!==undefined)this.#label=validateLabel(patch.label);if(patch.attributes!==undefined)this.#attributes=cloneAttributes(patch.attributes);}
  get [Symbol.toStringTag]():string{return'AtlasNode';}
  [Symbol.toPrimitive](hint:string):string { if(hint==='number')throw new TypeError('AtlasNode has no numeric primitive meaning');return this.id; }
  [ATLAS_INSPECT](_depth:number,options:InspectOptionsStylized):string{return `AtlasNode ${options.stylize(this.id,'special')} { kind: ${this.#kind}, label: ${JSON.stringify(this.#label)}, parent: ${this.#parentId??'root'}, children: ${this.#children.length}, attributes: ${Object.keys(this.#attributes).length} }`;}
}
