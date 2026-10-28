# Reference Answers — Module 05: Queries, Stable Pagination, and Authorized Access

Read after attempting all twelve Queries, Stable Pagination, and Authorized Access exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why must an order be total for cursor pagination?

The cursor needs a unique boundary. If rows compare equal, the next predicate cannot reliably decide which equal rows were already visited.

## 2. How does pure keyset pagination behave when a row appears before the boundary, and what extra rule does the capstone high-water value provide?

A row that sorts before the stored last key is not returned on later pages and does not shift existing rows as an offset would. The capstone adds a first-page high-water position, so rows inserted after traversal begins are also excluded because their monotonic positions are greater than that bound. This proves append-insertion stability, not a cross-request snapshot: deletion or a filter-relevant update can still change the remaining eligible set.

## 3. What semantic data belongs in a cursor fingerprint?

Stable operation ID, principal/owner, normalized filters, sort/direction, and any result-set policy that changes membership or order.

## 4. Why store server-side cursor handles instead of signed self-contained tokens?

An authoritative server-side row makes revocation, expiry, principal binding, filter binding, and policy changes direct. The decimal handle contains no trusted continuation data; modifying it only selects another row, which must still pass every context check. A signed self-contained token is a valid alternative that removes lookup state but adds key rotation, token-size, revocation, and canonicalization concerns. The reference handle is not described as cryptographically signed or confidential.

## 5. How can deletion between pages affect keyset traversal?

Deleting an unvisited row simply removes it; deleting the boundary row does not invalidate a tuple boundary stored in the cursor. Exact snapshot semantics would require stronger machinery.

## 6. Why is foreign ownership represented as not found?

It avoids existence disclosure and is implemented naturally by an owner-qualified query.

## 7. What is wrong with `ORDER BY ${sort}`?

Parameterized queries cannot parameterize identifiers, so interpolation creates injection and unapproved-column risk. Choose from trusted static fragments.

## 8. How should an expired cursor differ from a never-valid cursor?

The public contract may use the same stable invalid-cursor problem to avoid exposing storage state; internal evidence can distinguish reasons.

## 9. Why is `SELECT *` dangerous even with response validation?

It loads sensitive fields unnecessarily, increases coupling, and creates a second chance for serializer misconfiguration to leak them.

## 10. Design a pagination invariant.

Across traversal, every returned ID is unique, positions are strictly increasing, no row above the first-page high-water value appears, and the union equals the rows that were eligible at traversal start and remained eligible until visited. The final clause makes the limitation under deletion or filter-relevant mutation explicit.

## 11. Trace stable authorized pagination in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` and `capstone/tracks/typescript-fastify/src/repository.ts`. The required invariant is that cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry.

## 12. Compare stable authorized pagination across Python and TypeScript

Both tracks must preserve this invariant: cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry. The intentional difference is that Python may parse database integers directly; TypeScript preserves bigint cursor handles as strings until validated.
