import assert from 'node:assert/strict'; import test from 'node:test';
import { defineCatalog } from '../src/index.js';
const catalog=defineCatalog({id:'search',label:'Search',stability:'stable'},{id:'export',label:'Export',stability:'experimental'});
test('preserves literal IDs and runtime lookup',()=>{assert.deepEqual(catalog.ids(),['search','export']); assert.equal(catalog.get('search').label,'Search');});
test('rejects duplicate identifiers',()=>assert.throws(()=>defineCatalog({id:'x',label:'X',stability:'stable'},{id:'x',label:'Other',stability:'deprecated'}),/duplicate/));
if(false){
  // @ts-expect-error unknown IDs are not in the catalog contract
  catalog.get('missing');
}
