#!/usr/bin/env bash

# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/15836a106059cc8d201e1237adf44aec340bbab6/helm/crds-common/templates/giantswarm.yaml

MOCK_CREDENTIALS=$(echo -n "something" | base64)

export AWS_B64ENCODED_CREDENTIALS="${MOCK_CREDENTIALS}"

export AZURE_SUBSCRIPTION_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_TENANT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_ID_B64="${MOCK_CREDENTIALS}"
export AZURE_CLIENT_SECRET_B64="${MOCK_CREDENTIALS}"

export EXP_MACHINE_POOL="true"
clusterctl init --infrastructure=aws:v2.0.2,azure:v1.7.0
kubectl wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-aws -A
kubectl wait --for=condition=ready --timeout=90s pod -lcluster.x-k8s.io/provider=infrastructure-azure -A
