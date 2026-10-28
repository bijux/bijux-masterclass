import { resolve } from "node:path";

import { settingsFromEnvironment } from "./config.js";
import { applyMigrations } from "./migrations.js";

const settings = settingsFromEnvironment();
const target = process.env["MIGRATION_TARGET"];
const migrationsDirectory = resolve("migrations");

for (const revision of await applyMigrations(
    settings.databaseUrl,
    migrationsDirectory,
    target,
)) {
    console.log(revision);
}
