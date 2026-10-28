# Exercises — CNI lifecycle, IPAM, routes, and Node integration

Answer from first principles. Draw the packet path or ownership graph when it clarifies the answer. State which evidence would falsify your conclusion.

## 1. What does a successful CNI ADD prove?

## 2. Why must DEL tolerate a missing network namespace?

## 3. Which stable identities should bind an allocation record?

## 4. What risk does GC introduce if the runtime provides an incomplete known-good set?

## 5. Why can CHECK pass while the application is unreachable from another Node?

## 6. How does a chained CNI configuration complicate rollback?

## 7. Compare host-local and cluster-coordinated IPAM during a control-plane partition.

## 8. Why is address-pool exhaustion a capacity signal rather than an ordinary retry?

## 9. What evidence distinguishes a leaked allocation from a still-running partitioned sandbox?

## 10. Why should CNI and host firewall automation not share anonymous nftables chains?

## 11. What does STATUS need to evaluate beyond binary existence?

## 12. Why is CNI not the correct place to model HTTP routing?
