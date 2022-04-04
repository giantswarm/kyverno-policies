SHELL:=/usr/bin/env bash

# Kind cluster name to use
KIND_CLUSTER_NAME ?= "kyverno-cluster"

# If not already set through env
KUBERNETES_VERSION ?= v1.21.1

##@ Generate

.PHONY: generate
generate: ## Replace variables on Helm manifests.
	./hack/template.sh

.PHONY: verify
verify:
	@$(MAKE) generate
	git diff --exit-code

##@ Test

.PHONY: clean
clean: ## Delete test manifests from kind cluster.
	./hack/cleanup-local.sh

.PHONY: kind-create
kind-create: ## create kind cluster if needed
	KIND_CLUSTER_NAME=$(KIND_CLUSTER_NAME) ./hack/kind-with-registry.sh
	./hack/setup-kind.sh

.PHONY: tilt-up
tilt-up: ## Start Tilt
	tilt up

# If you change kyverno version here remember to change it in the Tiltfile too
.PHONY: install-kyverno
install-kyverno:
	kubectl create --context kind-$(KIND_CLUSTER_NAME) -f https://raw.githubusercontent.com/kyverno/kyverno/v1.5.1/definitions/release/install.yaml
	kubectl wait --context kind-$(KIND_CLUSTER_NAME) --for=condition=ready pod -l app=kyverno -nkyverno

.PHONY: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONY: dabs
dabs:  # generate
	dabs.sh --generate-metadata --chart-dir helm/kyverno-policies/charts/kyverno-policies
