#!/usr/bin/env node
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import process from "node:process";

const modulePath = process.env.TYPESCRIPT_LIB;
if (!modulePath) {
  console.error("TYPESCRIPT_LIB is required");
  process.exit(2);
}
const ts = await import(`file://${resolve(modulePath)}`);
const root = resolve(process.argv[2]);
const markdownFiles = [];
const excluded = new Set([
  ".git",
  ".pytest_cache",
  "__pycache__",
  "node_modules",
  ".venv",
  "site",
  "dist-core",
  ".runtime",
]);

function walk(directory) {
  for (const name of readdirSync(directory)) {
    if (excluded.has(name)) continue;
    const path = join(directory, name);
    const metadata = statSync(path);
    if (metadata.isDirectory()) walk(path);
    else if (path.endsWith(".md")) markdownFiles.push(path);
  }
}

walk(root);
const fence = /```([^\n`]*)\n([\s\S]*?)```/g;
const supported = new Set(["typescript", "ts", "javascript", "js"]);
const failures = [];
let fences = 0;
for (const path of markdownFiles.sort()) {
  const text = readFileSync(path, "utf8");
  let match;
  let localIndex = 0;
  while ((match = fence.exec(text)) !== null) {
    const language = (match[1].trim().split(/\s+/)[0] || "").toLowerCase();
    if (!supported.has(language)) continue;
    localIndex += 1;
    fences += 1;
    const scriptKind = ["javascript", "js"].includes(language)
      ? ts.ScriptKind.JS
      : ts.ScriptKind.TS;
    const source = ts.createSourceFile(
      `${relative(root, path)}#fence-${localIndex}`,
      match[2],
      ts.ScriptTarget.Latest,
      true,
      scriptKind,
    );
    for (const diagnostic of source.parseDiagnostics) {
      const location = source.getLineAndCharacterOfPosition(diagnostic.start ?? 0);
      failures.push(
        `${relative(root, path)} fence ${localIndex} ` +
          `${location.line + 1}:${location.character + 1}: ` +
          ts.flattenDiagnosticMessageText(diagnostic.messageText, " "),
      );
    }
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(JSON.stringify({ status: "passed", fences }));
