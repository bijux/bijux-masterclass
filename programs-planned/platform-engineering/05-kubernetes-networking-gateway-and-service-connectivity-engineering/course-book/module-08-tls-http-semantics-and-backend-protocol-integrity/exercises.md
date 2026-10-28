# Exercises — TLS, HTTP semantics, and backend protocol integrity

Answer from first principles. State the control-plane object, data-plane mechanism, failure mode, and decisive evidence.

## 1. What does TLS termination at the Gateway make the Gateway responsible for?

## 2. Why is backend TLS incomplete without hostname/SAN verification?

## 3. What does SNI influence?

## 4. Why should a Gateway replace incoming X-Forwarded-For?

## 5. How can retries multiply work?

## 6. When is retrying POST potentially safe?

## 7. What trade does response buffering create?

## 8. Why can a certificate rotate successfully in Kubernetes but remain stale in the proxy?

## 9. What is the difference between passthrough and re-encryption?

## 10. Why is an open TCP port not gRPC proof?

## 11. What does a 421 response communicate?

## 12. How should timeout values be related?
