import assert from'node:assert/strict';import test from'node:test';import{displayName,migrateUser,parseUser}from'../src/index.js';
test('reads both versions and migrates old responses',()=>{const old=parseUser({format:'USER_V1',id:'1',name:'Ada'});assert.equal(displayName(old),'Ada');assert.deepEqual(migrateUser(old),{format:'USER_V2',id:'1',displayName:'Ada',tags:[]});});
test('rejects unknown future formats explicitly',()=>assert.throws(()=>parseUser({format:'USER_V3',id:'1'}),/unsupported/));
// @ts-expect-error V2 requires tags
migrateUser({format:'USER_V2',id:'1',displayName:'Ada'});
