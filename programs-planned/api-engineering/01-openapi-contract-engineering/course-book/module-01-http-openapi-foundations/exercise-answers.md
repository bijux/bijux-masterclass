# Reference Answers — Module 01: HTTP and OpenAPI Foundations

Read after attempting all twelve HTTP and OpenAPI Foundations exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Write the complete raw request and response for creating a project named `Atlas`. Include the minimum fields that establish the contract.

A correct answer uses `POST /projects`, JSON content, `201 Created`, `Location`, a response content type, and a project representation. `200` or an omitted location loses creation semantics.

## 2. Classify each method as safe and/or idempotent: GET, POST, PUT, DELETE.

`GET` is safe and idempotent; `PUT` and `DELETE` are idempotent but not safe; `POST` is neither by method semantics, though a specific operation may add an idempotency mechanism.

## 3. Explain why an internal analytics counter does not make a GET operation unsafe.

Safety concerns the effect requested by the client. Incidental logging or accounting can occur, but the client must not request a state change through GET.

## 4. Find the structural error when `responses` is aligned with `get` rather than nested under it.

It becomes a Path Item field rather than an Operation response map. A strict parser or linter should reject or flag it.

## 5. Why can changing only `operationId` be breaking?

Generators commonly derive method names from it. Existing compiled or source consumers may no longer find the generated method even though the URL is unchanged.

## 6. Give one claim a parser can prove and one it cannot.

It can prove the description has a response map and resolvable references. It cannot prove the running provider returns that response.

## 7. Design a negative test for `/projects/{projectId}`.

Use an identifier violating the documented pattern and assert the public validation problem media type and status, then use a well-formed unknown ID and assert 404.

## 8. Why is a representation not the same as a resource?

The resource is the identified conceptual entity; JSON is one current representation that can vary by media type, time, or negotiated view.

## 9. Choose a stable operation ID for retrieving one project and justify it.

`getProject` is outcome-oriented, concise, and independent of framework/controller version. Names like `projectControllerGetV2` expose implementation.

## 10. What evidence would falsify the claim that project creation conforms?

Any observed mismatch in method/path acceptance, status, required headers, response media type, or response schema is enough.

## 11. Practical defect exercise

For **State-changing GET**, a valid solution must first reproduce: `GET /projects/{id}/delete` appears convenient but requests deletion. The smallest useful starting case is: send the GET request twice and observe the resource disappear. The repair is: Choose `DELETE` or a command resource and test retry semantics.

## 12. Cross-language parity exercise

The HTTP and OpenAPI Foundations parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
