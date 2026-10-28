import { describe, expect, it } from "vitest";

import { Database } from "../src/db.js";

const url = process.env["TEST_DATABASE_URL"];

describe.skipIf(!url)("PostgreSQL integration", () => {
  it("uses a real PostgreSQL transaction", async () => {
    const database = new Database(url!);
    try {
      const value = await database.transaction(async (client) => {
        const result = await client.query(
          "SELECT current_setting('server_version_num')::int AS version",
        );
        return Number(result.rows[0]?.version);
      });
      expect(value).toBeGreaterThanOrEqual(180000);
    } finally {
      await database.close();
    }
  });
});
