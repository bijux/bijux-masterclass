# Atlas Kubernetes Runtime 1.0

This capstone converts the immutable Atlas Workload Release from Course 3 into Kubernetes desired state and evidence.

The dependency-light lane is executable with Python and Go. The optional kind lane observes a real local control plane but is deliberately separated from the production-intent release. The capstone does not silently substitute a toy image or `emptyDir` and then claim that the inherited workload or durability contract was proven.

```bash
make capstone-tour
make python-test
make go-test
make manifest-policy-proof
```
