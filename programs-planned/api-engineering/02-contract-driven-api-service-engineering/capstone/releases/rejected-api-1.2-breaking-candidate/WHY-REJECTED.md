# Why this API 1.2.0 candidate is rejected

The candidate reuses the API 1.2.0 minor version while making three
consumer-visible breaking changes:

1. `callbackUrl` becomes required in `createAnalysisRun` requests.
2. `checksum` is removed from the accepted request algorithm enum.
3. `ownerId` is removed from run responses.

The release proof must identify all three changes at their actual operation
surfaces. A component-only diff is not sufficient evidence because an unused
component does not change consumer behavior.
