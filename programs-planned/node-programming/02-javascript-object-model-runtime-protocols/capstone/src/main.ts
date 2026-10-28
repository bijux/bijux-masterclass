#!/usr/bin/env node
import { execute } from './app.js';
import { parseCommand } from './command.js';
import { FileAtlasStore } from './storage.js';
async function main():Promise<void>{try{const command=parseCommand(process.argv.slice(2));const path=process.env.OBJECT_ATLAS_FILE??'object-atlas.json';const result=await execute(command,new FileAtlasStore(path));if(result.output!=='')process.stdout.write(`${result.output}\n`);}catch(error){const message=error instanceof Error?error.message:String(error);process.stderr.write(`objectatlas: ${message}\n`);process.exitCode=2;}}
await main();
