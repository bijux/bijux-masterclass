# Start here — Platform Engineering

Platform engineering is the design and operation of trusted capabilities that let other teams deliver and run software without rediscovering every systems problem. The program introduces abstractions only after the learner has studied the lower-layer mechanisms they hide.

The first five stages are:

```text
Atlas Host Runtime 1.0
→ Atlas Cloud Foundation 1.0
→ Atlas Workload Release 1.0
→ Atlas Kubernetes Workload 1.0
→ Atlas Connectivity Plane 1.0
```

Course 5 begins after Kubernetes can reconcile the Atlas API and worker workloads. It does not assume that Pods can already communicate correctly. It makes the packet path explicit: CNI attachment, IP allocation, routes, Services, EndpointSlices, DNS, policy, gateway attachment, TLS, egress, and topology decisions.

For every connection ask: which name or address did the caller use, which control-plane object declared intent, which data-plane component implemented it, which identity survived translation, and what observation proves the packet reached the intended peer?

Begin Course 5 at `05-kubernetes-networking-gateway-and-service-connectivity-engineering/course-book/start-here.md`.
