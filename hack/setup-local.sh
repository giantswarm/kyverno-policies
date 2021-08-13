#!/bin/bash

kind create cluster --image quay.io/giantswarm/kind-node:$1 --name kyverno-cluster
kubectl wait nodes/kyverno-cluster-control-plane --for=condition=ready --timeout=5m > /dev/null
kind get kubeconfig --name kyverno-cluster > $(pwd)/kube.config

apiextensionsVersion=v3.32.0
# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/$apiextensionsVersion/helm/crds-common/templates/giantswarm.yaml
# Giant Swarm upstream CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/$apiextensionsVersion/helm/crds-common/templates/upstream.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/$apiextensionsVersion/helm/crds-aws/templates/upstream.yaml

# CAPZ CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-azure/master/config/crd/bases/infrastructure.cluster.x-k8s.io_azureclusters.yaml
# Kyverno
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kyverno/kyverno/v1.4.1/definitions/release/install.yaml
