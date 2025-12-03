SHELL:=/usr/bin/env bash

# Kind cluster name to use
KIND_CLUSTER_NAME ?= "kyverno-cluster"

# These values should be set by the outer environment / CircleCI environment config.
KUBERNETES_VERSION ?= v1.30.13
KYVERNO_VERSION ?= v1.16.0

##@ Test

.PHONY: clean
clean: ## Delete test manifests from kind cluster.
	./hack/cleanup-local.sh

.PHONY: kind-create
kind-create: ## create kind cluster if needed
	KIND_CLUSTER_NAME=$(KIND_CLUSTER_NAME) ./hack/kind-with-registry.sh
# 	./hack/setup-kind.sh

.PHONY: tilt-up
tilt-up: ## Start Tilt
	tilt up

# If you change kyverno version here remember to change it in the Tiltfile too
.PHONY: install-kyverno
install-kyverno:
	kubectl create --context kind-$(KIND_CLUSTER_NAME) -f https://github.com/kyverno/kyverno/releases/download/$(KYVERNO_VERSION)/install.yaml
	kubectl wait --context kind-$(KIND_CLUSTER_NAME) --for=condition=ready pod -l app.kubernetes.io/name=kyverno -l app.kubernetes.io/component=admission-controller -n kyverno --timeout 300s

.PHONY: install-policies
install-policies:
	helm upgrade --install kyverno-policies ./helm/kyverno-policies --set "kyverno-policies.validationFailureAction=Enforce"

.PHONY: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONY: dabs
dabs:  # generate
	dabs.sh --generate-metadata --chart-dir helm/kyverno-policies
