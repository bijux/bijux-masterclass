# Exercises — NetworkPolicy and L3/L4 segmentation

Answer from first principles. Draw the packet path or ownership graph when it clarifies the answer. State which evidence would falsify your conclusion.

## 1. When does a Pod become isolated for ingress?

## 2. Why can adding a second policy not revoke traffic allowed by the first?

## 3. What is the semantic difference between one peer containing namespaceSelector plus podSelector and two separate peers?

## 4. Why is a label selector not proof of workload identity?

## 5. Why must DNS egress include TCP as well as UDP?

## 6. What does an allowed TCP port fail to authorize?

## 7. Why is ipBlock behavior around Services dangerous to assume?

## 8. What should be prepared before default deny?

## 9. Why can 0.0.0.0/0 egress undermine the exercise?

## 10. How do source egress and destination ingress policies combine?

## 11. Why might a node-local resolver require special handling?

## 12. What evidence proves NetworkPolicy enforcement?
