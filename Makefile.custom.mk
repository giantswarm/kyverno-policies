SHELL:=/usr/bin/env bash

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

.PHONY: setup
setup: ## Create kind cluster with CAPI and Kyverno.
	@$(MAKE) generate
	./hack/setup-local.sh $(KUBERNETES_VERSION)
