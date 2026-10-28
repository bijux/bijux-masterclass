# Worked answers

## 1. Why can a Node with low observed CPU still reject a Pod?

The scheduler uses declared requests and constraints, not momentary utilization. Existing requested capacity may leave insufficient allocatable CPU, or labels/taints/topology may filter the Node. The decisive evidence is scheduler filter reasons plus Node allocatable/requested state. Runtime dashboards alone do not explain scheduling.

## 2. How do CPU and memory limits differ operationally?

CPU limits normally throttle consumption over time, increasing latency. Memory limits can cause OOM termination when exceeded because memory cannot simply be delayed safely. Both require runtime/cgroup evidence. A Pod that repeatedly OOMs needs memory analysis; raising liveness thresholds does not repair it.

## 3. What makes a Pod Guaranteed QoS?

Every container must declare CPU and memory requests and limits, and each request must equal its corresponding limit. Missing one resource or unequal values makes the Pod Burstable. QoS affects eviction/OOM treatment but does not guarantee scheduling, survival, or service availability.

## 4. Why does a toleration not place a Pod on a tainted Node?

A toleration removes one repelling filter. The scheduler still considers labels, resources, affinity, topology, and scoring. If the design requires a dedicated pool, combine toleration with required affinity or selector. Otherwise the Pod may run on ordinary Nodes as well.

## 5. When is hard pod anti-affinity harmful?

It can make placement impossible when there are fewer topology domains than replicas or when labels are inconsistent. It is also expensive at scale. Use it only for non-negotiable separation; topology spread with explicit skew often gives better availability/capacity trade-offs.

## 6. What does maxSkew describe?

It bounds the difference in matching Pod counts among eligible topology domains according to the constraint’s semantics. It does not create domains or capacity. Missing labels, insufficient Nodes, and other filters can still make scheduling impossible. Evidence should show domain counts and eligibility.

## 7. Why might preemption be unhelpful?

Preemption only frees occupied resources. It cannot create a required label, remove an untolerated taint, add a topology domain, or satisfy volume/node compatibility. Scheduler evidence that preemption is not helpful points to hard constraints rather than reclaimable occupancy.

## 8. Why is nodeName usually inappropriate in an application manifest?

It bypasses normal scheduler selection and can ignore NoSchedule taints. It couples the Pod to one Node and defeats topology/capacity policy. Static or specialized cases may use it, but Atlas application placement should be expressed as constraints and left to the scheduler.

## 9. How can under-requesting increase eviction risk?

A Pod using substantially more than its request contributes to node pressure while appearing cheap to schedule. Under pressure, usage relative to requests influences eviction ranking for Burstable Pods. Accurate requests improve placement and make resource policy reflect actual needs.

## 10. Why is Course 3 resource data called a hypothesis?

It came from bounded course evidence, not representative load or production observation. Course 4 needs values to exercise scheduling and QoS, but must not promote them to capacity truth. Course 5 measures workload performance; Course 9 manages fleet capacity.

## 11. What is the minimum safe fix for an impossible constraint set?

The fix is the smallest change that preserves the actual placement and failure-domain intent: add matching capacity, correct an erroneous label/taint contract, adjust a measured request, or deliberately relax a topology rule. Removing all affinity/toleration/resource declarations hides the reason and weakens safety.

## 12. Why does kind not prove zone spreading?

A kind cluster usually runs nodes as containers on one host and does not provide independent cloud failure domains. Labels can simulate zones for scheduler behavior, but the failure isolation is fictional. The evidence can prove constraint processing, not zone availability.
