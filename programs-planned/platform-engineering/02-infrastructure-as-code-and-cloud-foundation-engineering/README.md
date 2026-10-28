# Infrastructure as Code and Cloud Foundation Engineering

**Course 2 of the Platform Engineering program**

This course turns the provider-neutral requirements from Linux, Networking, and Cloud Systems Engineering into a reproducible cloud foundation.

The main product is the [course book](course-book/start-here.md). The capstone is **Atlas Cloud Foundation 1.0**, an AWS reference lane expressed in OpenTofu with a dependency-light semantic model for learners who do not yet have a cloud sandbox.

The course teaches infrastructure as a stateful control process, not as a collection of resource blocks. By the end, the learner can design a landing-zone boundary, bootstrap and recover remote state, write useful modules, build a routed network, grant short-lived workload authority, provision replaceable compute, protect durable data, adopt existing infrastructure, refactor without replacement, and release changes through a controlled pipeline.

```bash
make help
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

Real AWS exercises are opt-in and cost-bearing. No default proof target creates cloud resources.
