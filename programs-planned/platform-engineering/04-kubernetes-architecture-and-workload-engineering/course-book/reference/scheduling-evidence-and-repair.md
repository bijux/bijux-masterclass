# Scheduling evidence and repair

Scheduling is a feasibility problem followed by scoring. A Pending Pod may fail several hard predicates on every Node.

## Inputs

Preserve:

- Pod requests and overhead;
- required node affinity and selectors;
- taints and tolerations;
- Pod affinity/anti-affinity;
- topology spread constraints;
- volume topology;
- host ports;
- Node allocatable and existing allocations;
- quota and priority/preemption context.

## Repair classification

- **Demand repair:** reduce a request after measurement shows it was overstated.
- **Capacity repair:** add or free feasible capacity.
- **Policy repair:** change affinity/spread only after accepting availability or isolation consequences.
- **Topology repair:** correct labels or add capacity in required domains.
- **Workload repair:** remove an unnecessary hard coupling.

Deleting the Pod is not a scheduling repair. Adding every toleration is not a safe repair. Increasing priority transfers pain to another workload.
