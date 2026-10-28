# Worked Answers — Module 06: Authorization, Tenancy, and Schema Exposure

Use these solutions to audit your reasoning for **Authorization, Tenancy, and Schema Exposure**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is successful parent resolution insufficient for child authorization?

Different fields expose different capabilities. Run visibility does not imply artifact download or delivery-detail permission.

**Decisive evidence.** Resolve a visible run without artifact permission. The parent must remain visible, the child becomes null with a stable error, and Artifact Service receives zero calls.

The chapter’s decisive distinction is this: A principal with RUN READ can read run status but lacks ARTIFACT READ. Selecting artifacts produces a field authorization outcome; the gateway never calls Artifact Service. A tenant-B identifier for a tenant-A run is concealed at the Analysis Control query boundary.

## 2. Where should tenant filtering occur for a list?

In the source-service query before rows, counts, and cursors are produced.

**Decisive evidence.** Inspect the owner-service query or batch request. Tenant and principal constraints must limit the source population before pagination, counting, or caching.

In the cumulative capstone, the rule becomes concrete: Filtering a fully loaded cross-tenant collection in the gateway is unsafe and inefficient. Analysis Control receives the principal and applies tenant ownership while selecting runs. The graph only sees authorized rows. This prevents count, timing, and pagination leakage.

## 3. Why is post-filtering in the gateway risky?

It can leak counts, timing, cursors, and memory usage and can accidentally paginate unauthorized rows.

**Decisive evidence.** Create more foreign rows than the requested page size. Gateway post-filtering will produce short pages, incorrect `hasNextPage`, and possible timing leakage; the test must expose this.

A useful way to reason about the boundary is: That approach produces timing and count leaks, sparse pages, incorrect cursors, and unnecessary exposure inside the graph process. The correct source method accepts tenant and policy scope and returns an already authorized ordered population.

## 4. Should introspection be disabled as the main defense?

No. Known operations still execute and schemas can leak elsewhere. Authorization and demand controls remain primary; introspection policy is contextual.

**Decisive evidence.** Run the same unauthorized operation with introspection enabled and disabled. Access must remain denied in both cases, proving introspection is not the authorization boundary.

The implementation consequence is: Introspection is a type-system capability, not an authorization system. Disabling introspection does not make fields secret; clients can still observe network behavior, documentation, generated clients, and error messages. The primary defenses are correct authorization, demand control, and removal of capabilities that should not exist.

## 5. What do trusted documents protect?

They restrict admitted operation documents and improve lifecycle and demand evidence. They do not authenticate the caller or authorize fields.

**Decisive evidence.** Attempt an unknown digest, an approved digest for the wrong client, and an approved operation with unauthorized variables/resources. Trusted documents control programs, not data permissions.

The important nuance is: Production environments may restrict arbitrary introspection for untrusted callers or expose a client-specific registry view. If so, the policy must account for IDEs, CI validation, incident debugging, and supported clients. The course favours trusted operations for public clients while retaining controlled schema inspection for development and governance.

## 6. How should a denied sensitive field behave?

Follow the declared policy: stable forbidden error or concealment, with no source call and no sensitive value in logs.

**Decisive evidence.** Choose and test one declared behavior: nullable field plus `FORBIDDEN`, concealed parent, or request rejection. The source call count must remain zero for denied fields.

Under concurrency or failure, the distinction becomes: The choice is product and security policy, but it must agree with nullability. A non-null sensitive field cannot be redacted to null without bubbling. Making it nullable creates room for policy denial but also requires clients to distinguish forbidden, unavailable, and absent through error codes or explicit state.

## 7. Why must batch loaders include tenant context?

A batch can otherwise mix identical local IDs across tenants and return the wrong value.

**Decisive evidence.** Load the same local ID through tenant A and tenant B contexts. The loader key or source API must prevent cache reuse across the authorization boundary.

The design remains honest only if: A GraphQL operation can select fields with different sensitivity under one root object. Authentication creates a principal and tenant context, but authorization must be evaluated for the actual selection. Granting access to AnalysisRun.id does not imply access to artifacts, downloadUrl, or delivery details.

## 8. Who decides a state-dependent cancellation policy?

Analysis Control, because it owns current run state and performs the atomic mutation. The gateway can enforce coarse permission first.

**Decisive evidence.** Attempt cancellation in queued, running, completed, and stale-version states. The graph policy delegates; Analysis Control remains the decision point.

The consumer-facing consequence is: The gateway delegates business authorization to the owner where the decision depends on current state. Edge policy can reject obviously missing permission, but the source service remains authoritative to avoid time-of-check/time-of-use defects.

## 9. What is schema visibility?

Serving or publishing a schema view appropriate to a client class. It reduces discovery but does not replace runtime authorization.

**Decisive evidence.** Compare public and privileged schema views or operation catalogues. Visibility may reduce discoverability, but any exposed coordinate still requires runtime authorization.

The operational consequence is: Introspection is a powerful development capability, not the primary security boundary. Disabling it does not stop known operations and can harm legitimate tooling. Production policy may expose one schema to trusted clients, client-specific schema views, or a published registry while restricting ad hoc exploration.

## 10. How can aliases interact with authorization?

Every aliased occurrence still resolves the same field policy. Authorization is based on coordinate and context, not response name.

**Decisive evidence.** Repeat a protected field under aliases and fragments. Policy must run on the field coordinate and source work must not multiply beyond admitted, authorized demand.

The strongest engineering interpretation is: The capstone keeps artifact fields nullable at the distributed boundary and attaches stable error extensions. It never returns an empty list for “forbidden,” because that claims the authorized set is authoritatively empty.

## 11. What is the correct response to a cross-tenant node ID?

Conceal or deny according to policy without revealing the foreign resource. The owner query should return no authorized object.

**Decisive evidence.** Submit a valid global ID from another tenant. Return the same not-found/concealed shape used for absent objects unless policy explicitly permits disclosure.

The defect-oriented view is: Singular lookups require the same care. An unauthorized global ID should not reveal whether an object exists through different errors, timing, type names, or cache behavior. The course policy uses consistent concealment for ordinary callers while allowing carefully audited administrative diagnostics through a separate capability.

## 12. What evidence proves no unauthorized source call occurred?

Call logs or trace spans assert zero Artifact Service call when the field permission is absent.

**Decisive evidence.** Capture source call logs while exercising missing permission, wrong tenant, and denied nested fields. The decisive count is zero before any protected key is dispatched.

Across the Python and TypeScript tracks, the invariant is: The HTTP layer authenticates the request and creates a principal. GraphQL validation proves that fields exist; it does not prove the caller may use them. Authorization is evaluated at root and nested fields because a caller may read a run but not artifact download URLs or delivery details.
