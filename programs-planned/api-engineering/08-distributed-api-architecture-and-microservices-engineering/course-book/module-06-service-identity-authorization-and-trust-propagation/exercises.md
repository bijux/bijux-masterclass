# Exercises — Module 06: Service Identity, Authorization, and Trust Propagation

Work through all twelve problems before opening the answers. In **Service Identity, Authorization, and Trust Propagation**, every response must settle this question: **How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?** Answer as though another team must implement and operate the design. Ambiguous ownership, unbounded behavior, and evidence-free claims are defects.

## 1. Why is workload identity insufficient to authorize an artifact upload?


## 2. What is the confused-deputy risk when Artifact Service trusts `X-User-Id`?


## 3. Why does a capability include audience?


## 4. Why bind an upload capability to checksum and maximum size?


## 5. Can mTLS replace resource authorization?


## 6. Why should the original public bearer token not automatically be forwarded to every service?


## 7. What context is safe to put in trace baggage?


## 8. Who performs the decisive artifact authorization?


## 9. Why must Control reauthorize completion after artifact upload?


## 10. What does network policy contribute?


## 11. How does short capability lifetime reduce coupling and risk?


## 12. Why is a shared internal superuser token unacceptable?

