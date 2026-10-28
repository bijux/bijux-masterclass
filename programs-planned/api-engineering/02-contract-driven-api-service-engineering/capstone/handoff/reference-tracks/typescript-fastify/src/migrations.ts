import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

import pg from "pg";

const { Client } = pg;
const MIGRATION_LOCK = 734_246_110;
const MIGRATION_NAME = /^\d{3}_.+[.]sql$/;

export async function migrationFiles(
  root: string,
  target?: string,
): Promise<string[]> {
  const files = (await readdir(root))
    .filter((name) => MIGRATION_NAME.test(name))
    .sort();
  if (files.length === 0) {
    throw new Error(`no migrations found under ${root}`);
  }

  const versions = files.map((name) => name.slice(0, 3));
  if (new Set(versions).size !== versions.length) {
    throw new Error("migration history contains duplicate numeric versions");
  }
  if (target !== undefined && !/^\d{3}$/.test(target)) {
    throw new Error("migration target must contain exactly three digits");
  }
  return target === undefined
    ? files
    : files.filter((name) => name.slice(0, 3) <= target);
}

/** Apply immutable, ordered SQL migrations while holding one advisory lock. */
export async function applyMigrations(
  url: string,
  root: string,
  target?: string,
): Promise<string[]> {
  const client = new Client({ connectionString: url });
  const applied: string[] = [];
  let lockHeld = false;

  await client.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version text PRIMARY KEY,
        checksum_sha256 text NOT NULL
          CHECK (checksum_sha256 ~ '^[0-9a-f]{64}$'),
        applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
      )
    `);
    await client.query("SELECT pg_advisory_lock($1)", [MIGRATION_LOCK]);
    lockHeld = true;

    for (const file of await migrationFiles(root, target)) {
      const bytes = await readFile(join(root, file));
      const checksum = createHash("sha256").update(bytes).digest("hex");
      const recorded = await client.query<{ checksum_sha256: string }>(
        `
          SELECT checksum_sha256
          FROM schema_migrations
          WHERE version = $1
        `,
        [file],
      );

      if (recorded.rowCount) {
        if (recorded.rows[0]?.checksum_sha256 !== checksum) {
          throw new Error(`applied migration changed on disk: ${file}`);
        }
        continue;
      }

      await client.query("BEGIN");
      try {
        await client.query(bytes.toString("utf8"));
        await client.query(
          `
            INSERT INTO schema_migrations(version, checksum_sha256)
            VALUES ($1, $2)
          `,
          [file, checksum],
        );
        await client.query("COMMIT");
        applied.push(file);
      } catch (error) {
        await client.query("ROLLBACK");
        throw error;
      }
    }
    return applied;
  } finally {
    if (lockHeld) {
      try {
        await client.query("SELECT pg_advisory_unlock($1)", [MIGRATION_LOCK]);
      } catch {
        // Connection termination also releases a session advisory lock.
      }
    }
    await client.end();
  }
}
