# Independent native-tool evidence lanes

The checked Python/Go capstone exposes OCI semantics without depending on a particular product. These scripts add independent evidence when the named tools and an isolated laboratory are available.

They are intentionally **not** invoked by `make core-proof`. Each script fails if its required tool or environment variable is missing. A missing tool is `not-executed`, never a pass.

| Script | Independent question |
|---|---|
| `buildkit-proof.sh` | Can an external OCI builder build the checked Containerfiles for both target platforms and export a valid OCI layout? |
| `runtime-proof.sh` | Can an external OCI runtime execute a generated bundle with the approved identity, mount, lifecycle, and cleanup contract? |
| `registry-proof.sh` | Can an operated registry preserve digest identity and subject-bound referrers under its real authentication/retention controls? |
| `supply-chain-proof.sh` | Can independent inventory, vulnerability, and signing tools produce and verify evidence for the exact release subject? |

Before running a lane, create an evidence directory outside the immutable course tree and record tool versions, host/kernel, target platform, credentials/identity scope, start/end time, and cleanup result. Never upload the public course signing key or fixture credentials to a real environment.
