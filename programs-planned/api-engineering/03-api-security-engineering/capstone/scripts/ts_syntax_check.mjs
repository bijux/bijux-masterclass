import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import process from "node:process";

const modulePath = process.env.TYPESCRIPT_LIB;
if (!modulePath) {
  console.error("TYPESCRIPT_LIB is required");
  process.exit(2);
}
const ts = await import(`file://${resolve(modulePath)}`);
const root = resolve(process.argv[2]);
const files = [];

function walk(directory) {
  for (const name of readdirSync(directory)) {
    if (["node_modules", "dist", "dist-core"].includes(name)) continue;
    const path = join(directory, name);
    const metadata = statSync(path);
    if (metadata.isDirectory()) walk(path);
    else if (path.endsWith(".ts")) files.push(path);
  }
}

walk(root);
const failures = [];
for (const path of files.sort()) {
  const source = ts.createSourceFile(
    path,
    readFileSync(path, "utf8"),
    ts.ScriptTarget.Latest,
    true,
    path.endsWith(".tsx") ? ts.ScriptKind.TSX : ts.ScriptKind.TS,
  );
  for (const diagnostic of source.parseDiagnostics) {
    const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, "\n");
    failures.push(`${path}:${diagnostic.start ?? 0}: ${message}`);
  }
}
if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(JSON.stringify({ status: "passed", files: files.length }));
