# Worked Answers — Module 05: Queries, Stable Pagination, and Authorized Access

Use these solutions to audit your reasoning for **Queries, Stable Pagination, and Authorized Access**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why must an order be total for cursor pagination?

The cursor needs a unique boundary. If rows compare equal, the next predicate cannot reliably decide which equal rows were already visited.

The chapter’s decisive distinction is this: A continuation boundary is meaningful only under an order that can compare every pair of rows. Non-unique sort keys need a deterministic tie-breaker. The capstone’s durable position provides a simple append order; name sorting pairs normalized name with position.

**Evidence.** Traverse multiple pages while inserting rows and changing principal or filters; assert stable high-water results and concealed foreign resources.

## 2. How does pure keyset pagination behave when a row appears before the boundary, and what extra rule does the capstone high-water value provide?

A row that sorts before the stored last key is not returned on later pages and does not shift existing rows as an offset would. The capstone adds a first-page high-water position, so rows inserted after traversal begins are also excluded because their monotonic positions are greater than that bound. This proves append-insertion stability, not a cross-request snapshot: deletion or a filter-relevant update can still change the remaining eligible set.

In the cumulative capstone, the rule becomes concrete: Evidence direction. Capture the first-page high-water position, insert later rows, and prove that the traversal returns each unchanged row from the original eligible set once while excluding positions above the captured high-water value.

## 3. What semantic data belongs in a cursor fingerprint?

Stable operation ID, principal/owner, normalized filters, sort/direction, and any result-set policy that changes membership or order.

A useful way to reason about the boundary is: A page belongs to one operation, principal, normalized filter set, sort specification, and continuation-consistency rule. The cursor must not silently continue a different set. The course fingerprints normalized filters and stores that identity with the continuation handle.

**Evidence.** Traverse multiple pages while inserting rows and changing principal or filters; assert stable high-water results and concealed foreign resources.

## 4. Why store server-side cursor handles instead of signed self-contained tokens?

An authoritative server-side row makes revocation, expiry, principal binding, filter binding, and policy changes direct. The decimal handle contains no trusted continuation data; modifying it only selects another row, which must still pass every context check. A signed self-contained token is a valid alternative that removes lookup state but adds key rotation, token-size, revocation, and canonicalization concerns. The reference handle is not described as cryptographically signed or confidential.

The implementation consequence is: A handle stores owner, operation, filter fingerprint, boundary, and expiry. This prevents token transfer and unbounded cursor-table growth. Expiry is a contract policy and must produce a stable error rather than a database miss with ambiguous meaning.

## 5. How can deletion between pages affect keyset traversal?

Deleting an unvisited row simply removes it; deleting the boundary row does not invalidate a tuple boundary stored in the cursor. Exact snapshot semantics would require stronger machinery.

The important nuance is: Evidence direction. Code review identifies every wide internal row read, public query paths use deliberate mapping/projection boundaries, and response tests inspect exact properties. A source grep is supporting evidence, not proof that secrets cannot escape.

**Evidence.** Traverse multiple pages while inserting rows and changing principal or filters; assert stable high-water results and concealed foreign resources.

## 6. Why is foreign ownership represented as not found?

It avoids existence disclosure and is implemented naturally by an owner-qualified query.

Under concurrency or failure, the distinction becomes: Ownership and scope requirements shape the SQL predicate and selected projection. A protected lookup should not fetch foreign data into application memory. This reduces accidental disclosure and aligns not-found concealment with one query.

**Counterexample.** A cursor is replayed under another principal or filter set, or concurrent inserts create duplicates and omissions.

**Evidence.** Traverse multiple pages while inserting rows and changing principal or filters; assert stable high-water results and concealed foreign resources.

## 7. What is wrong with `ORDER BY ${sort}`?

Parameterized queries cannot parameterize identifiers, so interpolation creates injection and unapproved-column risk. Choose from trusted static fragments.

The design remains honest only if: Choose the principle above most likely to fail in Queries, Stable Pagination, and Authorized Access . Compare the reference design with one credible alternative and name the counterexample that distinguishes their guarantees.

**Counterexample.** The service passes in one process but loses the invariant after restart, concurrency, or a partial dependency failure.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 8. How should an expired cursor differ from a never-valid cursor?

The public contract may use the same stable invalid-cursor problem to avoid exposing storage state; internal evidence can distinguish reasons.

The consumer-facing consequence is: The Queries, Stable Pagination, and Authorized Access increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 9. Why is `SELECT *` dangerous even with response validation?

It loads sensitive fields unnecessarily, increases coupling, and creates a second chance for serializer misconfiguration to leak them.

The operational consequence is: Queries select only fields required by the application result. Projection prevents persistence-only or secret columns from reaching serializers and can reduce I/O. It should be explicit rather than SELECT across evolving tables.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 10. Design a pagination invariant.

Across traversal, every returned ID is unique, positions are strictly increasing, no row above the first-page high-water value appears, and the union equals the rows that were eligible at traversal start and remained eligible until visited. The final clause makes the limitation under deletion or filter-relevant mutation explicit.

The strongest engineering interpretation is: Evidence direction. Capture the first-page high-water position, insert later rows, and prove that the traversal returns each unchanged row from the original eligible set once while excluding positions above the captured high-water value.

## 11. Trace stable authorized pagination in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` and `capstone/tracks/typescript-fastify/src/repository.ts`. The required invariant is that cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry.

The defect-oriented view is: The excerpt for Queries, Stable Pagination, and Authorized Access isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 12. Compare stable authorized pagination across Python and TypeScript

Both tracks must preserve this invariant: cursor state is bound to principal, operation, normalized filters, boundary, high-water position, and expiry. The intentional difference is that Python may parse database integers directly; TypeScript preserves bigint cursor handles as strings until validated.

Across the Python and TypeScript tracks, the invariant is: Claim Required evidence ---: --- --- 1 tie-heavy pages complete Write the narrow command and machine-readable oracle. 2 rows inserted after page one remain above the captured high-water value and do not enter the traversal Real PostgreSQL traversal report with returned IDs, positions, and cursor record 3 cursor bound to owner Write the narrow command and machine-readable oracle. 4 cursor bound to operation Write the narrow command and machine-readable oracle.
