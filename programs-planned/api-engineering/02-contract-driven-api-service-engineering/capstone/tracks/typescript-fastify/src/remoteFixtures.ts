import { lstat, realpath } from "node:fs/promises";
import { isAbsolute, join, relative, sep } from "node:path";

export class RemoteFixtureError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "RemoteFixtureError";
  }
}

/**
 * Resolve the course's controlled remote-object URI to a regular file.
 *
 * This adapter supports one HTTPS origin backed by an operator-controlled
 * fixture directory. It is deliberately not a general HTTP object-store
 * client.
 */
export async function resolveRemoteFixture(
  rootPath: string,
  uri: string,
): Promise<string> {
  const match = /^https:\/\/objects\.example\.test(\/[^?#]*)$/.exec(uri);
  if (!match) {
    throw new RemoteFixtureError("untrusted remote object URI");
  }
  const rawPath = match[1] ?? "";

  let decodedPath: string;
  try {
    decodedPath = decodeURIComponent(rawPath);
  } catch {
    throw new RemoteFixtureError("remote object path is not valid UTF-8");
  }
  if (decodedPath.includes("\\") || decodedPath.includes("\0")) {
    throw new RemoteFixtureError("remote object path contains an unsafe byte");
  }

  const segments = decodedPath.split("/").filter(Boolean);
  if (
    segments.length === 0 ||
    segments.some((segment) => segment === "." || segment === "..")
  ) {
    throw new RemoteFixtureError("remote object path traversal");
  }

  const root = await realpath(rootPath);
  let candidate = root;
  let finalMetadata: Awaited<ReturnType<typeof lstat>> | undefined;
  for (const segment of segments) {
    candidate = join(candidate, segment);
    finalMetadata = await lstat(candidate);
    if (finalMetadata.isSymbolicLink()) {
      throw new RemoteFixtureError("remote fixture contains a symbolic link");
    }
  }

  const resolved = await realpath(candidate);
  const relation = relative(root, resolved);
  if (
    relation === ".." ||
    relation.startsWith(`..${sep}`) ||
    isAbsolute(relation)
  ) {
    throw new RemoteFixtureError("remote fixture escaped root");
  }
  if (!finalMetadata?.isFile()) {
    throw new RemoteFixtureError("remote fixture is not a regular file");
  }
  return resolved;
}
