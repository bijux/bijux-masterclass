# Module 7 — Gateway API architecture and route ownership

The problem at the edge of a Kubernetes platform is not merely “how do I map a hostname to a Service?” The edge is where infrastructure authority, certificate authority, application routing, tenant boundaries, protocol behavior, and external reachability meet. If these concerns are compressed into one resource owned by one team, the configuration may be convenient, but the ownership model is usually weak.

Gateway API is valuable because it separates those concerns. It gives infrastructure providers a place to define implementation classes, platform teams a place to govern shared listeners, application teams a place to declare routes, and target namespaces a way to approve cross-namespace references. The resources are useful only when that separation is preserved. Installing the CRDs and copying an example manifest does not create a sound edge architecture.

The engineering question for this module is:

> How can several teams share an entry data plane while retaining explicit authority, deterministic routing, narrow references, and observable reconciliation?

## Learning outcomes

By the end of this module you should be able to:

- distinguish the responsibilities of GatewayClass, Gateway, Route, ReferenceGrant, controller, and data plane;
- explain the difference between an API object being stored, accepted, programmed, and reachable;
- reason about listener and Route attachment without relying on YAML proximity;
- evaluate hostname intersection, path matching, method/header predicates, and route precedence;
- review cross-namespace references as target-owned authority decisions;
- read status conditions using observed generation rather than treating one green condition as complete proof;
- define an implementation-specific conformance profile instead of claiming generic “Gateway API support”;
- decide when Ingress should remain during migration;
- design a release that preserves TLS, NetworkPolicy, backend ownership, and rollback boundaries.

## The architecture has six distinct parts

A complete path through Gateway API involves more than the four visible API resource families.

```text
Gateway API CRDs
        ↓
GatewayClass
        ↓
Gateway and listeners
        ↓
Routes and references
        ↓
controller reconciliation
        ↓
real data-plane configuration and external address
```

Each transition has a different owner and a different failure mode.

### Gateway API CRDs

The CRDs define which objects the API server can store and validate. Their presence proves only that the API surface exists. It does not prove that a controller watches the objects, that a GatewayClass is accepted, that a listener can be provisioned, or that any packet can reach a backend.

The Atlas baseline uses the Standard channel of Gateway API 1.6.1. Experimental resources and fields are not silently introduced into the release. When the course discusses an extended feature, the implementation profile must name it explicitly and the release evidence must distinguish it from the Standard baseline.

### GatewayClass

GatewayClass is cluster-scoped. It identifies the controller responsible for Gateways of that class and may refer to implementation parameters. It is an infrastructure selection boundary, not an application routing object.

A platform should normally limit who can create or modify GatewayClasses. If any namespace owner can register an arbitrary controller, the cluster has allowed application configuration to choose infrastructure code with cluster-wide effects. The class owner must also publish the implementation version, conformance profile, supported address types, and lifecycle policy.

### Gateway

A Gateway requests listeners and, depending on the implementation, addresses and infrastructure. The Gateway owner decides:

- which ports and protocols are exposed;
- which hostnames are served;
- where TLS terminates;
- which certificate references are allowed;
- which namespaces and Route kinds may attach;
- which GatewayClass and infrastructure parameters are used.

The Gateway therefore represents shared edge authority. It should not be casually delegated to every application team when listeners, addresses, or certificates are shared.

### Route

A Route expresses application traffic intent. HTTPRoute can declare hostnames, matches, filters, and backends. GRPCRoute and other Route kinds represent protocol-specific routing. A Route owner should be able to change application paths without gaining control of unrelated listeners or certificates.

A valid Route can still be unattached. A Route can also attach while one backend reference remains unresolved, or be accepted while the parent Gateway is not programmed. Route existence is not traffic evidence.

### ReferenceGrant

Cross-namespace references are denied unless the target namespace grants them. This direction matters. A source Route cannot grant itself access to another namespace’s Service or Secret. The target owner creates a ReferenceGrant describing which source group, kind, and namespace may refer to which target group and kind.

ReferenceGrant authorizes an API reference. It does not:

- allow packets through NetworkPolicy;
- authenticate the calling workload;
- authorize an application request;
- guarantee that the target Service has eligible endpoints;
- transfer ownership of the referenced object.

A broad ReferenceGrant can erase the ownership boundary. Treat grants as security-sensitive interfaces with owners, reasons, reviews, and retirement dates.

### Controller and data plane

The controller observes Gateway API objects and configures infrastructure or a proxy data plane. The data plane may be an in-cluster proxy, node-level implementation, cloud load balancer, managed Gateway, or another system. Controller health and proxy health are not the same thing.

A controller can accept configuration but fail to program a listener because an address cannot be allocated. A data plane can be programmed but unreachable because DNS, firewall, cloud routes, or external health checks are wrong. Gateway status narrows the search; it does not replace packet and protocol evidence.

## Attachment is a sequence of predicates

A Route does not attach because its `parentRefs` happens to name a Gateway. Evaluate attachment as an ordered decision:

1. **Parent identity** — does the reference identify the intended Gateway and, where specified, listener section?
2. **Route-kind permission** — does the listener accept this Route kind?
3. **Namespace permission** — does `allowedRoutes` admit the Route namespace?
4. **Hostname intersection** — do listener and Route hostnames intersect under the defined wildcard rules?
5. **Reference permission** — are cross-namespace backends or certificate references granted by the target namespace?
6. **Backend validity** — does the referenced Service and port exist and use a supported protocol relationship?
7. **Controller support** — does the selected implementation support the fields and filters used?
8. **Programming** — has the controller configured the listener and routes into the data plane?

The Atlas semantic model returns a reason for each rejected attachment and includes `observedGeneration`. That last field prevents a condition generated for an older specification from being mistaken for current evidence.

### Namespace selection is an authority surface

`allowedRoutes.namespaces` may admit Routes from the same namespace, all namespaces, or namespaces selected by labels. A label selector is not merely organizational metadata when it grants edge authority. The platform must control who may assign the relevant namespace labels and audit changes.

An unsafe pattern is to use a broadly assignable label such as `environment=production` as the only attachment gate. A tenant that can label its own namespace could attach to a shared production listener. Use labels whose mutation authority matches their security meaning.

### Hostname intersection is not string equality

A listener hostname and Route hostname must intersect. Wildcards are constrained to a single left-most label pattern. A broad wildcard listener can intentionally host many applications, but it also expands the set of Routes capable of competing for names. The ownership model must explain who allocates hostnames and how conflicts are prevented before they reach the controller.

DNS ownership, Gateway hostname configuration, and certificate coverage are separate. A Route can match a hostname that DNS does not point to the Gateway. A Gateway can serve a name not covered by its certificate. Course 8 will test these protocol boundaries.

## Route matching and precedence

Routing becomes dangerous when engineers reason from declaration order rather than specification-defined precedence. For every matching request, record the candidate set and the factors used to select the winner.

For an HTTP route, relevant dimensions can include:

- hostname intersection;
- exact versus prefix path match;
- path specificity;
- method match;
- header and query predicates;
- creation time or resource identity where the specification defines a tie-breaker;
- implementation-supported filters and features.

A safe review asks two questions:

1. Which request population is intended to match this rule?
2. Which other rule populations overlap it?

A catch-all `/` prefix is not inherently wrong. It is risky when a more specific route is assumed to win without an executable precedence test. The course’s matcher returns all candidates rather than only the winner so that shadowing is visible.

### Weighted backends are not a deployment safety system

Traffic weights express relative backend selection. They do not provide:

- compatibility checks;
- health or correctness gates;
- rollback criteria;
- state migration;
- idempotency safety;
- exact per-request counts;
- protection from retries changing observed proportions.

Course 7 of the program will govern delivery and progressive release. In Course 5, a weighted route is only a routing mechanism. A release must still prove backend compatibility and failure behavior.

### Filters alter application semantics

Rewrites, redirects, header modifications, mirroring, and retries can change what the backend observes. Examples:

- a path rewrite can bypass an application route that was expected to enforce authorization;
- a header modifier can create a trusted-looking identity header unless the backend trusts only the Gateway hop;
- request mirroring can disclose personal or secret data to an unapproved backend;
- retries can duplicate a non-idempotent operation;
- a redirect can move the client to another origin or protocol.

Every filter needs an owner and a semantic review, not only syntax validation.

## Status is a reconciliation ledger

Gateway API conditions are useful because they expose stages of reconciliation. Read them as a ledger, not a final boolean.

For each relevant condition, record:

- object and namespace;
- parent and listener section;
- condition type;
- `True`, `False`, or `Unknown` status;
- reason and message;
- observed generation;
- transition time;
- reporting controller.

Typical questions include:

- Is the GatewayClass accepted by the controller?
- Is the Gateway accepted?
- Is an address assigned?
- Is the listener programmed?
- Is the Route accepted by the listener?
- Are references resolved?
- Is the current generation represented?

Do not infer external reachability from `Programmed=True`. That condition means the controller believes it programmed its data plane. DNS, cloud firewall rules, upstream routing, health checks, TLS identity, and application behavior remain separate transitions.

## Conformance is feature-scoped

“Controller X supports Gateway API” is not a useful release statement. A defensible profile names:

- Gateway API version;
- Standard or Experimental channel;
- implementation and controller version;
- conformance profile;
- supported resources;
- supported core and extended features;
- skipped or failed conformance tests;
- environment and infrastructure provider;
- implementation-specific configuration;
- known deviations.

A controller can be conformant for a core profile and still lack a specific extended filter the application needs. Conversely, a non-core feature may work in one environment without being portable. The Atlas release records only the features it actually consumes.

## Gateway API and Ingress

Ingress remains a stable API and many mature controllers implement important behavior through annotations. A migration should not be driven by the belief that newer YAML is automatically better.

Gateway API is a stronger fit when the platform needs:

- explicit separation between infrastructure and application routing;
- multiple Route kinds;
- governed cross-namespace attachment;
- richer status and condition ownership;
- portable core features and conformance reporting;
- shared listeners without granting full listener control to every application.

Ingress may remain temporarily when the current controller provides proven behavior that the selected Gateway implementation does not yet provide. A safe migration runs both paths in bounded environments, compares protocol behavior, and preserves rollback. It does not delete the old edge after one successful request.

## Atlas ownership model

Atlas uses the following boundary:

| Artifact | Owner | Reason |
|---|---|---|
| GatewayClass | platform infrastructure team | selects controller and infrastructure implementation |
| shared HTTPS Gateway | platform networking team | owns address, listeners, shared TLS posture, and attachment policy |
| Atlas HTTPRoute | Atlas application team | owns application paths and backend intent |
| `atlas-api` Service | Atlas workload owner | owns endpoint contract and application port |
| cross-namespace ReferenceGrant | target namespace owner | grants narrow reference authority |
| DNS record | platform DNS owner | maps logical name to Gateway address |
| backend authorization | Atlas application/security owner | validates user and workload authority |

The baseline keeps the Route and backend Service in the same namespace. A separate laboratory introduces a cross-namespace backend so that ReferenceGrant behavior can be studied without making the production reference unnecessarily complex.

## Worked investigation — accepted Route, unreachable listener

An Atlas HTTPRoute reports:

```text
Accepted=True
ResolvedRefs=True
observedGeneration=7
```

Clients receive connection timeouts. The first response is often to edit Route matches or restart Atlas Pods. Neither action follows the evidence.

Construct the transition ledger:

| Transition | Result | Owner |
|---|---|---|
| Route stored and validated | pass | API server |
| listener admits Route namespace and hostname | pass | Gateway policy/controller |
| backend Service and port resolve | pass | Route/controller |
| Gateway obtains requested address | fail | infrastructure/controller |
| listener programmed into data plane | fail | controller/data plane |
| DNS points to reachable address | not reached | DNS owner |
| TLS/application exchange | not reached | edge/application |

The Gateway reports `Programmed=False` because its requested address class cannot be allocated in the current environment. Route acceptance is therefore truthful but incomplete. Editing path rules cannot create an external address. The repair belongs to the GatewayClass implementation or infrastructure parameters.

The lesson is general: start at the earliest failed transition. Gateway API provides ownership-rich status, but the engineer must still connect status to the real packet path.

## Laboratory and capstone increment

The Module 7 laboratory creates one authorized and one unauthorized Route. It proves:

- the authorized namespace and hostname attach;
- the unauthorized namespace is rejected by the listener;
- cross-namespace references require target-owned permission;
- route selection exposes all candidates and the winning precedence factors;
- a broad-listener planted defect is rejected by release policy.

The capstone adds:

- Standard-channel Gateway API resources;
- a platform-owned GatewayClass contract;
- a shared HTTPS Gateway;
- an application-owned HTTPRoute;
- a narrow ReferenceGrant example;
- machine-readable attachment evidence;
- an implementation conformance profile;
- an explicit boundary between stored API resources and executed data-plane evidence.

## Design review questions

Before approving a Gateway release, require answers to these questions:

1. Who may create or mutate GatewayClasses?
2. Who owns each listener and certificate reference?
3. Which namespaces and Route kinds may attach, and who controls the admitting labels?
4. How are hostnames allocated and conflicts prevented?
5. Which cross-namespace references exist, and has each target owner granted them narrowly?
6. Which filters change request semantics?
7. Which implementation features are core, extended, or implementation-specific?
8. Which status conditions reflect the current generation?
9. What proves the data plane and external address are reachable?
10. What is the rollback path if the new Gateway implementation fails?

A release that cannot answer these questions has routing configuration, not a governed edge architecture.

## Design a Gateway topology from authority, not convenience

Before writing resources, list the authorities that must remain separate:

- cluster infrastructure and controller selection;
- listener addresses, ports, protocols, and certificates;
- hostname allocation;
- application path and method routing;
- cross-namespace backend consent;
- backend Service ownership;
- DNS publication;
- external firewall and load-balancer configuration.

Then assign each authority to a team and Kubernetes object. A shared Gateway is useful when the platform owns listeners and certificates while application teams own Routes. A dedicated Gateway is useful when one product needs independent address, lifecycle, or protocol policy. Neither model is universally superior.

The anti-pattern is a shared object edited by several teams without field or process ownership. Gateway API separates resource roles, but it does not automatically create an organizational operating model.

## Migration from Ingress needs behavioral comparison

An Ingress-to-Gateway migration should compare observed behavior, not only translate fields:

- hostname and path precedence;
- redirects and rewrites;
- regular-expression or implementation-specific matches;
- request and response header changes;
- body limits and buffering;
- WebSocket, HTTP/2, and gRPC behavior;
- source identity and trusted forwarding headers;
- TLS certificate selection and rotation;
- health checks, timeouts, retries, and draining;
- status and external address publication.

Run old and new paths in parallel where possible, use synthetic clients with explicit authority and TLS verification, and define rollback before changing DNS. An annotation with no Gateway API equivalent is an architectural decision, not a string to copy into another field.

## Cross-namespace references form a consent graph

ReferenceGrant makes the target namespace the authority that grants a source namespace permission to refer to a kind of object. Model these grants as a directed graph and audit broad edges.

A safe review asks:

- Is the source namespace stable and controlled?
- Is the granted target kind narrower than necessary?
- Can the source select any object of that kind in the target namespace?
- Is the grant temporary or permanent?
- Which owner removes it when the relationship ends?
- Does NetworkPolicy still restrict packet reachability?
- Does application authorization remain intact?

A grant can make a reference valid while every packet is still denied. Conversely, a broad network path can exist while the API reference is not authorized. Both proofs are required.

## Route status must be correlated with infrastructure status

Route `Accepted=True` and `ResolvedRefs=True` are important but bounded observations. A complete path correlates:

- GatewayClass acceptance;
- Gateway acceptance and address assignment;
- listener conditions;
- Route parent status for the current generation;
- reference resolution;
- Service and EndpointSlice eligibility;
- controller data-plane configuration;
- DNS answer;
- external routing and firewall state;
- TLS and application response.

This correlation prevents a common operational loop in which application owners inspect Routes while platform owners inspect load balancers and neither records the first missing transition.

## Transition

Gateway API establishes who may declare listeners, routes, and references. Module 8 follows the request through those listeners and examines TLS identity, HTTP authority, backend protocol, timeout budgets, forwarding headers, buffering, and retry safety.
