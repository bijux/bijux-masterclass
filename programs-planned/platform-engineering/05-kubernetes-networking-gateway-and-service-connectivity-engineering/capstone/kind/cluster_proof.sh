#!/usr/bin/env bash
set -euo pipefail
: "${ALLOW_KIND_NETWORK_LAB:?set ALLOW_KIND_NETWORK_LAB=1 after reading the safety boundary}"
[[ "$ALLOW_KIND_NETWORK_LAB" == 1 ]]
for cmd in kind kubectl; do command -v "$cmd" >/dev/null || { echo "missing $cmd" >&2; exit 2; }; done
ctx="kind-atlas-networking-lab"
[[ "$(kubectl config current-context)" == "$ctx" ]] || { echo "refusing context $(kubectl config current-context)" >&2; exit 3; }
kubectl get nodes -o wide
kubectl get gatewayclass,gateway,httproute -A
kubectl get service,endpointslice,networkpolicy -A
