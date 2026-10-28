# Worked answers — Authorization, Tenancy, and Schema Exposure

Compare the decision rule and evidence, not just wording.

## 1. Why is successful parent resolution insufficient for child authorization?

Different fields expose different capabilities. Run visibility does not imply artifact download or delivery-detail permission.

**Decisive evidence.** Resolve a visible run without artifact permission. The parent must remain visible, the child becomes null with a stable error, and Artifact Service receives zero calls.

## 2. Where should tenant filtering occur for a list?

In the source-service query before rows, counts, and cursors are produced.

**Decisive evidence.** Inspect the owner-service query or batch request. Tenant and principal constraints must limit the source population before pagination, counting, or caching.

## 3. Why is post-filtering in the gateway risky?

It can leak counts, timing, cursors, and memory usage and can accidentally paginate unauthorized rows.

**Decisive evidence.** Create more foreign rows than the requested page size. Gateway post-filtering will produce short pages, incorrect `hasNextPage`, and possible timing leakage; the test must expose this.

## 4. Should introspection be disabled as the main defense?

No. Known operations still execute and schemas can leak elsewhere. Authorization and demand controls remain primary; introspection policy is contextual.

**Decisive evidence.** Run the same unauthorized operation with introspection enabled and disabled. Access must remain denied in both cases, proving introspection is not the authorization boundary.

## 5. What do trusted documents protect?

They restrict admitted operation documents and improve lifecycle and demand evidence. They do not authenticate the caller or authorize fields.

**Decisive evidence.** Attempt an unknown digest, an approved digest for the wrong client, and an approved operation with unauthorized variables/resources. Trusted documents control programs, not data permissions.

## 6. How should a denied sensitive field behave?

Follow the declared policy: stable forbidden error or concealment, with no source call and no sensitive value in logs.

**Decisive evidence.** Choose and test one declared behavior: nullable field plus `FORBIDDEN`, concealed parent, or request rejection. The source call count must remain zero for denied fields.

## 7. Why must batch loaders include tenant context?

A batch can otherwise mix identical local IDs across tenants and return the wrong value.

**Decisive evidence.** Load the same local ID through tenant A and tenant B contexts. The loader key or source API must prevent cache reuse across the authorization boundary.

## 8. Who decides a state-dependent cancellation policy?

Analysis Control, because it owns current run state and performs the atomic mutation. The gateway can enforce coarse permission first.

**Decisive evidence.** Attempt cancellation in queued, running, completed, and stale-version states. The graph policy delegates; Analysis Control remains the decision point.

## 9. What is schema visibility?

Serving or publishing a schema view appropriate to a client class. It reduces discovery but does not replace runtime authorization.

**Decisive evidence.** Compare public and privileged schema views or operation catalogues. Visibility may reduce discoverability, but any exposed coordinate still requires runtime authorization.

## 10. How can aliases interact with authorization?

Every aliased occurrence still resolves the same field policy. Authorization is based on coordinate and context, not response name.

**Decisive evidence.** Repeat a protected field under aliases and fragments. Policy must run on the field coordinate and source work must not multiply beyond admitted, authorized demand.

## 11. What is the correct response to a cross-tenant node ID?

Conceal or deny according to policy without revealing the foreign resource. The owner query should return no authorized object.

**Decisive evidence.** Submit a valid global ID from another tenant. Return the same not-found/concealed shape used for absent objects unless policy explicitly permits disclosure.

## 12. What evidence proves no unauthorized source call occurred?

Call logs or trace spans assert zero Artifact Service call when the field permission is absent.

**Decisive evidence.** Capture source call logs while exercising missing permission, wrong tenant, and denied nested fields. The decisive count is zero before any protected key is dispatched.
