kind create cluster --image quay.io/giantswarm/kind-node:$1 --name kyverno-cluster
kubectl wait nodes/kyverno-cluster-control-plane --for=condition=ready --timeout=5m > /dev/null
kind get kubeconfig --name kyverno-cluster > $(pwd)/kube.config
# Giant Swarm CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/15836a106059cc8d201e1237adf44aec340bbab6/helm/crds-common/templates/giantswarm.yaml
# Prometheus operator CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/prometheus-operator-app/master/helm/prometheus-operator-app/crds/crd-servicemonitors.yaml
# CAPI CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.3/config/crd/bases/cluster.x-k8s.io_clusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.3/config/crd/bases/cluster.x-k8s.io_machinedeployments.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.3/bootstrap/kubeadm/config/crd/bases/bootstrap.cluster.x-k8s.io_kubeadmconfigs.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/master/config/crd/bases/cluster.x-k8s.io_clusters.yaml
# CAPA CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/main/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/main/config/crd/bases/infrastructure.cluster.x-k8s.io_awsmachinetemplates.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/main/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusterroleidentities.yaml
# CAPZ CRDs
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-azure/master/config/crd/bases/infrastructure.cluster.x-k8s.io_azureclusters.yaml
# Kyverno
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kyverno/kyverno/v1.4.1/definitions/release/install.yaml
