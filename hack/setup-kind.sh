#!/usr/bin/env bash

# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/15836a106059cc8d201e1237adf44aec340bbab6/helm/crds-common/templates/giantswarm.yaml

# Prometheus operator CRDs
# kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/prometheus-operator-app/master/helm/prometheus-operator-app/crds/crd-servicemonitors.yaml

MOCK_CREDENTIALS=$(echo -n "something" | base64)

export AWS_B64ENCODED_CREDENTIALS="${MOCK_CREDENTIALS}"

export AZURE_SUBSCRIPTION_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_TENANT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_SECRET_B64="${MOCK_CREDENTIALS}"

export EXP_MACHINE_POOL="true"
clusterctl init --infrastructure=aws:v0.7.2,azure:v0.5.3
kubectl wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-aws -A
kubectl wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-azure -A
