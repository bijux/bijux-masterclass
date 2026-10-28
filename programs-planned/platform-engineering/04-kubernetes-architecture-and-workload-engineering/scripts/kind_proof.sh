#!/usr/bin/env bash
set -euo pipefail
COURSE=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
for tool in kind kubectl docker; do
  command -v "$tool" >/dev/null || { echo "NOT-EXECUTED: missing $tool"; exit 2; }
done
: "${ALLOW_KIND_PROOF:?set ALLOW_KIND_PROOF=1 for a disposable cluster}"
export KUBECONFIG="$COURSE/capstone/reports/kind-kubeconfig"
cluster=atlas-course4
cleanup() { kind delete cluster --name "$cluster" >/dev/null 2>&1 || true; rm -f "$KUBECONFIG"; }
trap cleanup EXIT
kind create cluster --config "$COURSE/capstone/kind/cluster.yaml" --image "kindest/node:v1.36.1@sha256:3489c7674813ba5d8b1a9977baea8a6e553784dab7b84759d1014dbd78f7ebd5"
kubectl create namespace atlas-system
kubectl apply -f "$COURSE/capstone/kind/observation-workload.yaml"
kubectl rollout status deployment/atlas-observation -n atlas-system --timeout=180s
kubectl get deployment,replicaset,pod -n atlas-system -o yaml > "$COURSE/capstone/reports/kind-objects.yaml"
kubectl get events -n atlas-system --sort-by=.metadata.creationTimestamp -o yaml > "$COURSE/capstone/reports/kind-events.yaml"
echo "PASS kind observation proof; this is not Course 3 binary or production evidence"
