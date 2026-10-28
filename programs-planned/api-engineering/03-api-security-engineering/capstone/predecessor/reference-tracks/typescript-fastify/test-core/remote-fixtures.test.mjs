import assert from "node:assert/strict";
import { mkdir, mkdtemp, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  RemoteFixtureError,
  resolveRemoteFixture,
} from "../dist-core/remoteFixtures.js";

async function root() {
  return mkdtemp(join(tmpdir(), "cdse-remote-fixture-"));
}

test("resolves a regular file under the approved origin", async () => {
  const fixtureRoot = await root();
  await mkdir(join(fixtureRoot, "cohort"));
  const target = join(fixtureRoot, "cohort", "reads.csv");
  await writeFile(target, "sample,value\na,1\n");

  const resolved = await resolveRemoteFixture(
    fixtureRoot,
    "https://objects.example.test/cohort/reads.csv",
  );

  assert.equal(resolved, target);
});

for (const uri of [
  "http://objects.example.test/cohort/reads.csv",
  "https://evil.example.test/cohort/reads.csv",
  "https://user@objects.example.test/cohort/reads.csv",
  "https://objects.example.test:444/cohort/reads.csv",
  "https://objects.example.test/cohort/reads.csv?version=1",
  "https://objects.example.test/cohort/reads.csv#part",
  "https://objects.example.test/%2e%2e/secret.txt",
  "https://objects.example.test/cohort/../secret.txt",
]) {
  test(`rejects unsafe remote URI: ${uri}`, async () => {
    const fixtureRoot = await root();
    await assert.rejects(
      resolveRemoteFixture(fixtureRoot, uri),
      RemoteFixtureError,
    );
  });
}

test("rejects a symbolic link in a path component", async (context) => {
  const fixtureRoot = await root();
  const outside = await root();
  await writeFile(join(outside, "reads.csv"), "secret");
  try {
    await symlink(outside, join(fixtureRoot, "cohort"), "dir");
  } catch (error) {
    context.skip(`symbolic links are unavailable: ${String(error)}`);
    return;
  }

  await assert.rejects(
    resolveRemoteFixture(
      fixtureRoot,
      "https://objects.example.test/cohort/reads.csv",
    ),
    /symbolic link/,
  );
});
