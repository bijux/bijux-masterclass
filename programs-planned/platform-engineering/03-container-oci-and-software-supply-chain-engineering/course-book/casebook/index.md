# Incident casebook

The casebook contains failures that cannot be understood by asking only whether an image built or a scanner passed. Each incident crosses at least two boundaries. That is deliberate: production container failures usually emerge where individually reasonable mechanisms are composed incorrectly.

| Case | The tempting conclusion | The actual defect |
|---|---|---|
| [The image that was not the container](the-image-that-was-not-the-container.md) | “The image was hardened, therefore the workload was isolated.” | Launch-time authority overrode image defaults. |
| [The secret deleted from the final layer](secret-deleted-from-final-layer.md) | “The file is gone from the final filesystem.” | Immutable earlier layer bytes still contained the credential. |
| [The multi-platform index lied](multiarch-index-lied.md) | “The descriptor says arm64, therefore it is an arm64 workload.” | Cache scope produced an amd64 executable under an arm64 label. |
| [The tag moved after approval](tag-moved-after-approval.md) | “Version 1.0.0 was approved.” | The mutable tag selected different bytes at deployment time. |
| [Signed by the wrong builder](signed-by-the-wrong-builder.md) | “The signature is valid, therefore the release is trusted.” | The signer and build identity were valid but unauthorized for production. |

## How to study a case

For each incident, produce four diagrams before reading the resolution:

1. **Object graph** — which source, layer, manifest, index, tag, digest, evidence object, and runtime request existed?
2. **Authority graph** — who could build, push, retag, sign, approve, launch, mount, or override?
3. **Time line** — when did identity, evidence, policy, and runtime configuration change?
4. **Proof gap** — which claim was accepted without an oracle capable of rejecting it?

Then answer two questions. First, which control would have prevented the incident? Second, which independent evidence would have detected it even if prevention failed? A mature release system needs both.
