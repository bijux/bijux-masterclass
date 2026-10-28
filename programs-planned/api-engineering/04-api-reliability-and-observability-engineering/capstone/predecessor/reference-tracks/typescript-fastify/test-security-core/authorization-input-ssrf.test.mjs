import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { authorize } from "../dist-security/security/authorization.js";
import { confinedPath, validateFilename, validateArchiveMembers } from "../dist-security/security/input-security.js";
import { validateDestination, verifyConnectedPeer } from "../dist-security/security/ssrf.js";

const capstone = new URL("../../../", import.meta.url);
const load = async (relative) => JSON.parse(await readFile(new URL(relative,capstone),"utf8"));
function policies(rows){return new Map(rows.map((r)=>[r.operationId,{operationId:r.operationId,scopes:new Set(r.scopes),roles:new Set(r.roles),relationship:r.relationship,tenantBound:r.tenantBound,conceal:r.concealment==="concealed",requiredAssurance:r.assurance,maxAuthAgeSeconds:r.freshAuthentication?300:undefined}]));}
function principal(raw){return raw===null||raw===undefined?undefined:{subject:raw.sub,tenant:raw.tenant,scopes:new Set(raw.scopes??[]),roles:new Set(raw.roles??[]),assurance:raw.assurance??"baseline",authAgeSeconds:raw.authAgeSeconds??0};}
function resource(raw){return {tenant:raw.tenant,owner:raw.owner,members:new Set(raw.members??[]),creator:raw.creator,status:raw.status};}

test("authorization vectors and default deny", async()=>{
 const matrix=await load("security-case/policy-matrix.json"); const auth=await load("shared/vectors/authorization.json"); const map=policies(matrix.policies);
 for(const item of auth.cases){const result=authorize(item.operationId,principal(item.principal),resource(item.resource??{}),map);assert.equal(result.allowed,item.allow,item.id);if(item.conceal)assert.equal(result.conceal,true);}
 assert.equal(authorize("unmapped",principal({sub:"u",tenant:"t",scopes:["all"]}),resource({tenant:"t",owner:"u"}),map).allowed,false);
});

test("path, filename and archive vectors", async()=>{
 const data=await load("shared/vectors/input-security.json");
 for(const item of data.pathCases){if(item.valid)assert.equal(confinedPath(item.root,item.value,item.decode??true),item.result,item.id);else assert.throws(()=>confinedPath(item.root,item.value,item.decode??true),undefined,item.id);}
 for(const item of data.filenameCases){if(item.valid)assert.equal(validateFilename(item.value),item.value);else assert.throws(()=>validateFilename(item.value));}
 for(const item of data.archiveCases){const options={maxMembers:item.maxMembers,maxTotalBytes:item.maxTotal};if(item.valid)assert.doesNotThrow(()=>validateArchiveMembers(item.members,options));else assert.throws(()=>validateArchiveMembers(item.members,options));}
});

test("SSRF vectors and peer binding", async()=>{
 const data=await load("shared/vectors/ssrf.json");
 for(const item of data.cases){const input={url:item.url,addresses:item.addresses,allowedPorts:item.allowedPorts??[443]};if(item.valid){const result=validateDestination(input);assert.doesNotThrow(()=>verifyConnectedPeer(result,item.addresses[0]));}else assert.throws(()=>validateDestination(input),undefined,item.id);}
 const result=validateDestination({url:"https://hooks.example.test/x",addresses:["93.184.216.34"]}); assert.throws(()=>verifyConnectedPeer(result,"8.8.8.8"));
});
