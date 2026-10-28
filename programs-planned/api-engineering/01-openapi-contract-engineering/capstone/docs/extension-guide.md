# Extension guide

A capstone extension is accepted only when it preserves the evidence architecture.

## Add an operation

1. Write the canonical Path Item and reusable schemas.
2. Add valid and invalid fixtures before provider code.
3. Add the operation ID to both providers.
4. Add behavior to the shared live suite.
5. Update the security matrix.
6. assess client-generation support.
7. run compatibility checks against the last release.
8. update Arazzo only when the operation changes outcome flow.

## Add a field

State whether it is request, response, or shared; whether missing differs from null; whether it is server-owned; whether it narrows accepted input; and whether generated consumers are closed. Add fixtures for the boundary, not only one happy example.

## Add a tool

Document the exact claim it proves, pin the version, add a failing planted case, surface missing installation as failure, and preserve its report. A redundant command that adds no independent claim is not an improvement.
