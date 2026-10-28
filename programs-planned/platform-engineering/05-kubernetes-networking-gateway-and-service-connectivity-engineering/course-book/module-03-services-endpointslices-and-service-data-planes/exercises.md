# Exercises — Services, EndpointSlices, and service data planes

Answer from first principles. Draw the packet path or ownership graph when it clarifies the answer. State which evidence would falsify your conclusion.

## 1. Why are Service, EndpointSlice, and node data-plane state three separate proof objects?

## 2. What does a correct selector fail to prove?

## 3. Why can existing connections outlive endpoint removal?

## 4. When is a headless Service appropriate?

## 5. Why is “no iptables rule” insufficient evidence of a broken Service?

## 6. What failure can a named targetPort prevent compared with a numeric targetPort?

## 7. Why can ClientIP affinity overload one backend behind NAT?

## 8. What must be measured during readiness withdrawal?

## 9. Why should a selectorless Service be reviewed as an authority boundary?

## 10. How does a LoadBalancer Service differ from Gateway API?

## 11. What does externalTrafficPolicy Local trade?

## 12. Why should Service release evidence record data-plane generation?
