# Worked answers — Gateway API architecture and route ownership

These answers separate API storage, attachment, programming, and real reachability. A green condition is useful only when its scope and generation are understood.

## 1. What authority does a GatewayClass represent?

GatewayClass selects the controller and infrastructure class responsible for Gateways that reference it. It can determine implementation code, parameters, address behavior, supported features, and lifecycle, so it is a cluster-level infrastructure authority rather than an application route. Creation and mutation should be restricted to the platform owner. A complete proof records the controller name/version, accepted status, conformance profile, parameters, and who can change the class. A stored GatewayClass without an accepting controller proves only that the API object exists.

## 2. Why can an accepted HTTPRoute still have no effect?

`Accepted=True` on the Route means the relevant parent/listener accepted the route under its attachment rules for the observed generation. The Gateway may still lack an address, listener programming may have failed, the data plane may be unreachable, DNS may point elsewhere, backend references may later fail, or the Service may have no eligible endpoints. Read the Route parent status together with GatewayClass, Gateway listener, `Programmed`, address, reference, Service, and packet evidence. Acceptance is one transition, not end-to-end success.

## 3. Who grants a cross-namespace backend reference?

The target namespace grants it through ReferenceGrant. A Route in a source namespace cannot authorize itself to refer to another namespace’s Service or other target. This direction preserves target ownership. The grant should narrowly identify source group, kind, and namespace and target group/kind, with a documented owner and reason. Prove that the authorized source resolves and that another namespace is rejected. The grant validates an API reference; it does not grant network or application authorization.

## 4. What does ReferenceGrant not provide?

It does not make packets reachable, create NetworkPolicy allows, authenticate workloads, authorize application operations, prove backend health, or transfer ownership of the target. It says only that a named class of source object from a source namespace may reference a target kind in the granting namespace. A complete path still needs Service/endpoints, data-plane programming, policy, TLS/protocol, and application authorization. Test an authorized reference with denied network traffic to demonstrate the distinction.

## 5. Why is Gateway API not just a newer Ingress syntax?

Gateway API separates infrastructure class, shared listener ownership, application route ownership, target consent, status, protocol-specific resources, and conformance profiles. Ingress typically combines fewer roles and often relies on implementation annotations. The value is the authority and reconciliation model, not merely different fields. A migration must compare behavior—routing precedence, TLS, headers, timeouts, retries, streaming, and source identity—rather than translating YAML mechanically. Ingress may remain when its proven behavior is not yet available in the chosen Gateway implementation.

## 6. What must a conformance claim name?

Name the Gateway API version and channel, implementation/controller and version, conformance profile, supported resources, core/extended features actually used, environment, conformance suite revision, passed/skipped/failed cases, and known deviations. “Supports Gateway API” is too broad. A controller can support core HTTPRoute while lacking an extended filter or BackendTLSPolicy feature Atlas needs. The release claim must be no stronger than the tested feature set and environment.

## 7. Why should route matching evidence show all candidates?

Showing only the selected route can hide overlapping hostnames, path prefixes, methods, headers, or catch-all rules that shadow another owner’s intent. The evidence should list every matching candidate and the specification-defined precedence factors that selected the winner. This makes ambiguity and future conflicts visible. Test near-boundary requests—for example `/api`, `/api/`, and a broader `/` route—rather than one happy path. Declaration order should not be assumed to control precedence unless the specification explicitly says so.

## 8. How can a broad hostname create an authority problem?

A wildcard or unrestricted listener can admit Routes for a large name space. If namespace labels or hostname allocation are weakly governed, another team can attach a competing Route or claim a name it does not own. DNS ownership and certificate coverage may also diverge. Restrict listener hostnames, govern namespace attachment labels, maintain a hostname allocation registry, and test unauthorized Route attachment. A wildcard certificate does not itself authorize every namespace to route every matching name.

## 9. Why is weighted routing not a release strategy by itself?

Weights distribute selections among backends, but they do not prove compatibility, correctness, health, state migration, rollback, idempotency, or exact traffic percentages under retries and long-lived connections. A canary release needs comparison metrics, user/request populations, abort criteria, and a safe rollback. Weighted routing is one mechanism inside that process. Test that both backends satisfy the same contract and that failure does not trigger retry amplification that distorts the intended distribution.

## 10. What does observedGeneration protect against?

It ties a status condition to the specification generation the controller evaluated. Without it, an old `Accepted=True` or `Programmed=True` condition can be mistaken for evidence about a newer object spec. During incident review, compare metadata generation with each condition’s observed generation. If they differ, the controller has not yet reported on current desired state. This is especially important after listener, hostname, backend, or certificate changes.

## 11. When should Ingress remain temporarily?

Keep it when the existing path has required, proven behavior that the selected Gateway implementation cannot yet reproduce safely, or when migration evidence and rollback are incomplete. Run old and new edges in parallel where possible, compare TLS, routing, headers, timeouts, streaming, source identity, and failure behavior, then shift DNS/traffic gradually. Temporary coexistence needs an owner and retirement criteria; it should not become permanent duplicate authority.

## 12. Why should application teams not own shared Gateway listeners by default?

Listeners control shared addresses, ports, protocols, certificate references, attachment policy, and often infrastructure cost and security posture. Allowing one application team to mutate them can affect unrelated tenants and names. Application teams should normally own Routes and backend intent, while the platform owns shared GatewayClass and listener infrastructure. A dedicated Gateway may be appropriate when an application genuinely needs independent lifecycle and authority. The boundary should follow blast radius and ownership, not convenience.
