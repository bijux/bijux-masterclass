# How to read a Kubernetes object

A large Kubernetes object is easier to understand when read in ownership order rather than top to bottom.

## 1. Establish identity

Read `apiVersion`, `kind`, namespace, name, and UID. Name is reusable; UID identifies this incarnation. Record resource version only as an opaque concurrency/watch token.

## 2. Identify desired-state authority

Read `spec`, then managed fields. Ask which actor owns each policy-bearing field. For a generated Deployment, the custom controller may own the Pod template while an autoscaler owns replicas. A value without an authority model is unstable.

## 3. Trace lifecycle ownership

Inspect owner references and finalizers. Owner references explain who controls deletion and child adoption. Finalizers explain which cleanup obligations keep deletion pending.

## 4. Compare desired and observed generations

If status reports an observed generation older than metadata generation, the controller has not yet reported processing the latest desired state. Do not interpret old status as evidence about the new intent.

## 5. Read conditions as a history of decisions

Use condition type, status, reason, message, observed generation, and transition time together. A message alone is not a stable API. A condition can say that progress is blocked without identifying the original root cause.

## 6. Follow child populations

For controllers, compare selector, owner reference, template hash, desired count, current count, ready count, and available count. Confirm that the objects you inspect actually belong to the controller.

## 7. Locate the earliest missing transition

Follow API admission, child creation, scheduling, node realization, container state, readiness, and endpoint eligibility. Diagnose at the first absent transition.

## 8. Preserve evidence before mutation

Capture the admitted object, conditions, managed fields, events, child UIDs, Pod states, Node placement, and logs before deleting or force-applying. A mutation can erase the evidence needed to distinguish causes.
