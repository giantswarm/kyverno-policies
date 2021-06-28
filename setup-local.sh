kind create cluster --name kyverno-cluster
kind get kubeconfig --name kyverno-cluster > ./kube.config
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kyverno/kyverno/main/definitions/release/install.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/giantswarm/apiextensions/b9a6bed05850045530eaf8ba7fd01941de6c8525/helm/crds-common/templates/giantswarm.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.3/config/crd/bases/cluster.x-k8s.io_clusters.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/release-0.3/config/crd/bases/cluster.x-k8s.io_machinedeployments.yaml
kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/main/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusters.yaml
