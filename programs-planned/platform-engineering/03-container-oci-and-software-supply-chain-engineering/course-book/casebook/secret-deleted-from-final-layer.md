# Incident case — the secret deleted from the final layer

## Situation

A build copied `.npmrc` into the image, installed private dependencies, and then removed the file in a later instruction. Final-rootfs inspection showed no credential. The image was signed, approved, and mirrored to a partner registry. Months later, a partner extracted an earlier layer and recovered the registry token.

The team initially argued that deletion should have been sufficient because a running container could no longer open the path. That argument confused the merged filesystem view with the immutable distribution history.

## What the image graph preserved

A layer is a filesystem changeset. The first layer stored the secret bytes. A later layer added a deletion/whiteout entry that hid the path in the merged rootfs. The old compressed blob remained reachable through the manifest’s ordered layer descriptors. Anyone authorized to pull the image graph could retrieve and inspect it.

The exposure surface was larger than one registry. Build caches, remote cache exports, mirrors, developer machines, CI artifacts, provenance parameters, logs, and scanner uploads may also have retained the value. Deleting a tag did not revoke digest access or erase downstream copies.

## Investigation method

1. Freeze promotion and preserve the exact index and platform manifests.
2. Enumerate every layer digest in order.
3. Decompress and inspect each layer independently, not only the merged rootfs.
4. Search configuration history, build logs, cache exports, provenance, and registry replication targets.
5. Determine the token’s authority and lifetime.
6. Revoke and rotate it before waiting for perfect exposure enumeration.
7. Identify every image/build derived from the contaminated cache or context.
8. Publish replacement subjects and record the old digests as revoked.

A secret scan against only the final rootfs would reproduce the original blind spot. The oracle must inspect immutable history.

## Correct build design

The credential is no longer part of the build context. The builder exposes it through a secret mount only to the dependency-fetch vertex. That vertex is configured so neither output nor shared cache contains the credential. Logs are reviewed for command echoing, URLs, and error output. A canary fixture secret is injected in CI; the release gate proves it cannot be recovered from source context, layers, configs, attestations, logs, or cache exports.

## Transfer lesson

Secret hygiene is a graph property. “Absent from the final filesystem” is a runtime-view claim. “Never persisted in any distributable or retained build object” is a much stronger supply-chain claim and needs a different proof.
