#!/usr/bin/env bash
set -euo pipefail

if [[ "${ALLOW_KIND_NETWORK_PROOF:-0}" != "1" ]]; then
  echo "Refusing privileged cluster proof. Set ALLOW_KIND_NETWORK_PROOF=1." >&2
  exit 2
fi
for tool in kind kubectl helm cilium; do
  command -v "$tool" >/dev/null || {
    echo "missing tool: $tool" >&2
    exit 3
  }
done

COURSE_DIR=$(cd "$(dirname "$0")/../.." && pwd)
CLUSTER=atlas-networking-lab
cleanup() {
  kind delete cluster --name "$CLUSTER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

if kind get clusters 2>/dev/null | grep -Fxq "$CLUSTER"; then
  echo "refusing to reuse existing kind cluster $CLUSTER" >&2
  exit 4
fi

kind create cluster --config "$COURSE_DIR/capstone/kind/cluster.yaml"
kubectl apply -f \
  "https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.1/standard-install.yaml"

helm upgrade --install cilium oci://quay.io/cilium/charts/cilium \
  --version 1.20.0 \
  --namespace kube-system \
  -f "$COURSE_DIR/capstone/cilium/values.yaml" \
  --set k8sServiceHost="${CLUSTER}-control-plane"

cilium status --wait
kubectl wait --for=condition=Ready nodes --all --timeout=180s
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/00-namespace-labels.yaml"
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/10-api-service.yaml"
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/11-api-service-prefer-close.yaml"
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/20-networkpolicy-default-deny.yaml"
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/21-networkpolicy-dns.yaml"
kubectl apply -f "$COURSE_DIR/capstone/manifests/base/22-networkpolicy-gateway-api.yaml"

kubectl get gatewayclass cilium >/dev/null
cat <<'EOF'
PASS local cluster foundation:
- dual-stack kind cluster created with kube-proxy disabled;
- Cilium owns CNI, NetworkPolicy, Service translation, and Gateway controller roles;
- Gateway API 1.6.1 Standard CRDs are established;
- namespace, Service, and policy contracts are stored.

The Course 4 workload images and TLS Secret are intentionally not fabricated by
this proof. Load the verified workload artifacts, create atlas-public-tls in
`gateway-system`, and apply the Gateway/HTTPRoute objects before making route or
TLS claims.
EOF
