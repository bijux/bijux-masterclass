# Exercises — Service Identity, Authorization, and Trust Propagation

Answer before reading the worked answers. Every answer must name the governing invariant and decisive evidence.

## 1. Why is workload identity insufficient to authorize an artifact upload?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 2. What is the confused-deputy risk when Artifact Service trusts `X-User-Id`?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 3. Why does a capability include audience?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 4. Why bind an upload capability to checksum and maximum size?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 5. Can mTLS replace resource authorization?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 6. Why should the original public bearer token not automatically be forwarded to every service?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 7. What context is safe to put in trace baggage?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 8. Who performs the decisive artifact authorization?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 9. Why must Control reauthorize completion after artifact upload?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 10. What does network policy contribute?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 11. How does short capability lifetime reduce coupling and risk?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 12. Why is a shared internal superuser token unacceptable?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.
