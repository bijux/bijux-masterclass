import { createHmac } from "node:crypto";
import { SecretBytes, redact } from "./secrets.js";

function canonical(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.entries(value as Record<string,unknown>).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>`${JSON.stringify(k)}:${canonical(v)}`).join(",")}}`;
}
export function pseudonym(value:string,key:SecretBytes):string{return createHmac("sha256",key.reveal()).update(value,"utf8").digest("hex").slice(0,24)}
export interface AuditEvent { sequence:number; occurredAt:string; actor:string; action:string; target?:string; decision:string; reason:string; correlationId:string; context?:Record<string,unknown> }
export class AuditChain {
  previousDigest="0".repeat(64); readonly records: Record<string,unknown>[]=[];
  constructor(private readonly key:SecretBytes){}
  append(event:AuditEvent):Record<string,unknown>{
    const payload:Record<string,unknown>={sequence:event.sequence,occurredAt:event.occurredAt,actor:event.actor,action:event.action,target:event.target??null,decision:event.decision,reason:event.reason,correlationId:event.correlationId,context:redact(event.context??{}),previousDigest:this.previousDigest};
    const eventDigest=createHmac("sha256",this.key.reveal()).update(canonical(payload),"utf8").digest("hex"); const record={...payload,eventDigest}; this.records.push(record); this.previousDigest=eventDigest; return record;
  }
  verify():boolean{let previous="0".repeat(64); for(const record of this.records){const {eventDigest,...payload}=record; if(payload.previousDigest!==previous) return false; const expected=createHmac("sha256",this.key.reveal()).update(canonical(payload),"utf8").digest("hex"); if(eventDigest!==expected) return false; previous=expected;} return true;}
}
