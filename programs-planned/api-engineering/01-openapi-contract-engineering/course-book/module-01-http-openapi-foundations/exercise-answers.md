# Worked Answers — Module 01: HTTP and OpenAPI Foundations

Use these solutions to audit your reasoning for **HTTP and OpenAPI Foundations**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Write the complete raw request and response for creating a project named `Atlas`. Include the minimum fields that establish the contract.

A correct answer uses `POST /projects`, JSON content, `201 Created`, `Location`, a response content type, and a project representation. `200` or an omitted location loses creation semantics.

The chapter’s decisive distinction is this: A project is the conceptual resource. /projects/prj 0001 is one identifier for it. The JSON document returned today is a representation of its current state. An OpenAPI Path Item groups operations addressable through one path template; it is not the resource itself.

## 2. Classify each method as safe and/or idempotent: GET, POST, PUT, DELETE.

`GET` is safe and idempotent; `PUT` and `DELETE` are idempotent but not safe; `POST` is neither by method semantics, though a specific operation may add an idempotency mechanism.

In the cumulative capstone, the rule becomes concrete: GET is defined as safe: the client does not request a state change. PUT, DELETE, and safe methods are idempotent in their intended effect; POST is not automatically idempotent. These properties affect retry behavior, caches, prefetchers, and generated client expectations.

## 3. Explain why an internal analytics counter does not make a GET operation unsafe.

Safety concerns the effect requested by the client. Incidental logging or accounting can occur, but the client must not request a state change through GET.

A useful way to reason about the boundary is: GET is defined as safe: the client does not request a state change. PUT, DELETE, and safe methods are idempotent in their intended effect; POST is not automatically idempotent. These properties affect retry behavior, caches, prefetchers, and generated client expectations.

## 4. Find the structural error when `responses` is aligned with `get` rather than nested under it.

It becomes a Path Item field rather than an Operation response map. A strict parser or linter should reject or flag it.

The implementation consequence is: Indentation is therefore semantic in YAML. Moving responses one level can turn an operation response map into an unknown Path Item field. A renderer may recover or omit the mistake; a parser and structural validator must reject it.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 5. Why can changing only `operationId` be breaking?

Generators commonly derive method names from it. Existing compiled or source consumers may no longer find the generated method even though the URL is unchanged.

The important nuance is: Many generators turn operationId: createProject into a method named create project or createProject. Renaming it while leaving POST /projects unchanged can break consumers. The capstone requires global uniqueness and tests provider handler maps against the canonical operation ledger.

**Evidence.** Diff the old and candidate contract in the correct request/response direction, then run active consumer or generated-client checks before promotion.

## 6. Give one claim a parser can prove and one it cannot.

It can prove the description has a response map and resolvable references. It cannot prove the running provider returns that response.

Under concurrency or failure, the distinction becomes: A specification can parse while the provider returns 200 instead of 201, emits text/plain, accepts undocumented input, or leaks an internal field. Conversely, a working provider may have no complete contract. Static checks prove document properties; live checks prove observed behavior.

## 7. Design a negative test for `/projects/{projectId}`.

Use an identifier violating the documented pattern and assert the public validation problem media type and status, then use a well-formed unknown ID and assert 404.

The design remains honest only if: This distinction prevents designs such as /getProjectObject or /callCreateProject. Paths should remain stable when handler classes, frameworks, and storage models change. Representations may evolve under compatibility rules, while resource identity and operation identity require deliberate migration.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 8. Why is a representation not the same as a resource?

The resource is the identified conceptual entity; JSON is one current representation that can vary by media type, time, or negotiated view.

The consumer-facing consequence is: A project is the conceptual resource. /projects/prj 0001 is one identifier for it. The JSON document returned today is a representation of its current state. An OpenAPI Path Item groups operations addressable through one path template; it is not the resource itself.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 9. Choose a stable operation ID for retrieving one project and justify it.

`getProject` is outcome-oriented, concise, and independent of framework/controller version. Names like `projectControllerGetV2` expose implementation.

The operational consequence is: For HTTP and OpenAPI Foundations, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 10. What evidence would falsify the claim that project creation conforms?

Any observed mismatch in method/path acceptance, status, required headers, response media type, or response schema is enough.

The strongest engineering interpretation is: For every HTTP and OpenAPI Foundations claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 11. Practical defect exercise

For **State-changing GET**, a valid solution must first reproduce: `GET /projects/{id}/delete` appears convenient but requests deletion. The smallest useful starting case is: send the GET request twice and observe the resource disappear. The repair is: Choose `DELETE` or a command resource and test retry semantics.

The defect-oriented view is: This HTTP and OpenAPI Foundations increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

## 12. Cross-language parity exercise

The HTTP and OpenAPI Foundations parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: For HTTP and OpenAPI Foundations, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.
