import assert from'node:assert/strict';import test from'node:test';import{defineLibrary,numberField,textField,type Output}from'../src/index.js';
const Score=defineLibrary({id:textField(),score:numberField()});
test('keeps runtime parse, inferred output, and deterministic format aligned',()=>{const value=Score.parse({id:'a',score:2});assert.deepEqual(value,{id:'a',score:2});assert.equal(Score.format(value),'id=a;score=2');assert.throws(()=>Score.parse({id:'a',score:'2'}),/finite/);});
type Score=Output<{readonly id:ReturnType<typeof textField>;readonly score:ReturnType<typeof numberField>}>;const value:Score={id:'a',score:2};void value;
// @ts-expect-error score remains numeric
Score.format({id:'a',score:'2'});
