import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { SecretBytes, redact } from "../dist-security/security/secrets.js";
import { signWebhook, verifyWebhook, MemoryReplayStore } from "../dist-security/security/webhooks.js";
import { AuditChain, pseudonym } from "../dist-security/security/audit.js";
import { TokenBucket, ConcurrencyLimiter } from "../dist-security/security/abuse.js";
import { Incident } from "../dist-security/security/incident.js";
const vectors=new URL("../../../../shared/vectors/",import.meta.url);const load=async(n)=>JSON.parse(await readFile(new URL(n,vectors),"utf8"));

test("exact-byte webhook, freshness and replay",async()=>{const data=await load("webhook.json");const secret=new SecretBytes(data.secret);const item=data.cases[0];const body=new TextEncoder().encode(item.body);const sig=signWebhook({secret,timestamp:item.timestamp,deliveryId:item.deliveryId,keyId:item.keyId,body});const replay=new MemoryReplayStore();verifyWebhook({body,timestamp:item.timestamp,deliveryId:item.deliveryId,keyId:item.keyId,signature:sig,now:item.timestamp,keys:new Map([[item.keyId,secret]]),replay});assert.throws(()=>verifyWebhook({body,timestamp:item.timestamp,deliveryId:item.deliveryId,keyId:item.keyId,signature:sig,now:item.timestamp,keys:new Map([[item.keyId,secret]]),replay}));const altered=new TextEncoder().encode(data.cases[1].body);assert.throws(()=>verifyWebhook({body:altered,timestamp:item.timestamp,deliveryId:item.deliveryId+"x",keyId:item.keyId,signature:sig,now:item.timestamp,keys:new Map([[item.keyId,secret]]),replay:new MemoryReplayStore()}));});

test("redaction and audit chain",async()=>{for(const item of (await load("redaction.json")).cases)assert.deepEqual(redact(item.input),item.expected,item.id);const key=new SecretBytes("audit-key");const chain=new AuditChain(key);chain.append({sequence:1,occurredAt:"2026-08-06T12:00:00Z",actor:pseudonym("u",key),action:"run.create",decision:"allow",reason:"policy.allow",correlationId:"r1",context:{authorization:"Bearer abc.def.ghi"}});assert.equal(chain.records[0].context.authorization,"[REDACTED]");assert.equal(chain.verify(),true);chain.records[0].reason="changed";assert.equal(chain.verify(),false);});

test("abuse vectors and permit release",async()=>{for(const item of (await load("abuse.json")).bucketCases){const bucket=new TokenBucket(item.capacity,item.refillPerSecond);for(const event of item.events)assert.equal(bucket.allow(event.atMs,event.cost),event.allow,item.id);}const limiter=new ConcurrencyLimiter(1);const permit=limiter.tryAcquire();assert(permit);assert.equal(limiter.tryAcquire(),undefined);permit.release();permit.release();assert.equal(limiter.inUse,0);});

test("incident state, revocation and key overlap",()=>{const incident=new Incident("INC-1");incident.record({at:"2026-08-06T09:00:00Z",source:"alert",statement:"fixture",confidence:"confirmed"});incident.transition("triaged");incident.revokeToken("stolen-jti");incident.rotateWebhookKey("whk-2026-02",true);assert(incident.verificationKeys.has("whk-2026-01"));incident.transition("contained");incident.retireWebhookKey("whk-2026-01");incident.transition("recovered");incident.transition("closed");assert(incident.revokedTokenIds.has("stolen-jti"));});
