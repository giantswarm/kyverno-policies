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
	./hack/apply-crds.sh

.PHONE: tilt-up
tilt-up: kind-create ## Start Tilt
	tilt up

.PHONE: install-kyverno
install-kyverno:
	kubectl create --context kind-kyverno-cluster -f https://raw.githubusercontent.com/kyverno/kyverno/v1.5.1/definitions/release/install.yaml

.PHONE: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONE: dabs
dabs: generate
	dabs.sh --generate-metadata --chart-dir helm/policies-common
	dabs.sh --generate-metadata --chart-dir helm/policies-aws
	dabs.sh --generate-metadata --chart-dir helm/policies-azure
	dabs.sh --generate-metadata --chart-dir helm/policies-vsphere
	dabs.sh --generate-metadata --chart-dir helm/policies-shared
