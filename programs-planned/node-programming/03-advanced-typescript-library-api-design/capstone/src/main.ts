#!/usr/bin/env node
import { readFile, rename, writeFile, unlink } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { canonicalJson, parseJson } from './json.js';
import { migrateProject, Project } from './project.js';
import { formatIssues } from './core.js';
import { SCHEMAKIT_VERSION } from './version.js';

async function main(args: readonly string[]): Promise<number> {
  const [command, ...rest] = args;
  if (command === undefined || command === 'help' || command === '--help') {
    process.stdout.write(help());
    return 0;
  }
  if (command === 'version' || command === '--version') {
    process.stdout.write(`schemakit ${SCHEMAKIT_VERSION}\n`);
    return 0;
  }
  if (command === 'example') {
    process.stdout.write(canonicalJson({ format: 'SCHEMAKIT_PROJECT_V2', name: 'Example', tags: ['typescript'] }));
    return 0;
  }
  if (command === 'check' && rest.length === 1) {
    const path = resolve(rest[0]!);
    const text = await readFile(path, 'utf8');
    const result = Project.safeParse(parseJson(text, path));
    if (!result.ok) {
      process.stderr.write(`${formatIssues(result.issues)}\n`);
      return 1;
    }
    process.stdout.write(`${result.value.format}: ${result.value.name}\n`);
    return 0;
  }
  if (command === 'normalize' && rest.length === 2) {
    const inputPath = resolve(rest[0]!);
    const outputPath = resolve(rest[1]!);
    const raw = parseJson(await readFile(inputPath, 'utf8'), inputPath);
    const project = migrateProject(Project.parse(raw));
    await replaceFile(outputPath, canonicalJson(project));
    process.stdout.write(`${outputPath}\n`);
    return 0;
  }
  process.stderr.write(`invalid command\n\n${help()}`);
  return 2;
}

async function replaceFile(path: string, content: string): Promise<void> {
  const temporary = join(dirname(path), `.${process.pid}.${Date.now()}.schemakit.tmp`);
  try {
    await writeFile(temporary, content, { encoding: 'utf8', flag: 'wx' });
    await rename(temporary, path);
  } catch (error: unknown) {
    await unlink(temporary).catch(() => undefined);
    throw error;
  }
}

function help(): string {
  return [
    'SchemaKit',
    '',
    'schemakit check <project.json>',
    'schemakit normalize <input.json> <output.json>',
    'schemakit example',
    'schemakit help',
    'schemakit version',
    '',
  ].join('\n');
}

main(process.argv.slice(2)).then(
  (code) => { process.exitCode = code; },
  (error: unknown) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 2;
  },
);
