#!/usr/bin/env bash

# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/15836a106059cc8d201e1237adf44aec340bbab6/helm/crds-common/templates/giantswarm.yaml

# Prometheus operator CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/prometheus-operator-app/master/helm/prometheus-operator-app/crds/crd-servicemonitors.yaml

# CAPI CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_machinedeployments.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_machinesets.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_machines.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_machinehealthchecks.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_machinepools.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/cluster.x-k8s.io_clusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/addons.cluster.x-k8s.io_clusterresourcesetbindings.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/config/crd/bases/addons.cluster.x-k8s.io_clusterresourcesets.yaml

# Bootstrap
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/bootstrap/kubeadm/config/crd/bases/bootstrap.cluster.x-k8s.io_kubeadmconfigs.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/bootstrap/kubeadm/config/crd/bases/bootstrap.cluster.x-k8s.io_kubeadmconfigtemplates.yaml

# ControlPlane
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.4/controlplane/kubeadm/config/crd/bases/controlplane.cluster.x-k8s.io_kubeadmcontrolplanes.yaml

# CAPA CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/release-0.7/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/release-0.7/config/crd/bases/infrastructure.cluster.x-k8s.io_awsmachinetemplates.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/release-0.7/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusterroleidentities.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/release-0.7/config/crd/bases/infrastructure.cluster.x-k8s.io_awsmachinepools.yaml

# CAPZ CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-azure/release-0.5/config/crd/bases/infrastructure.cluster.x-k8s.io_azureclusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-azure/release-0.5/config/crd/bases/infrastructure.cluster.x-k8s.io_azuremachinepools.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-azure/release-0.5/config/crd/bases/infrastructure.cluster.x-k8s.io_azuremachinetemplates.yaml
