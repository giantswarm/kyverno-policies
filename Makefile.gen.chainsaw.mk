# DO NOT EDIT. Generated with:
#
#    devctl
#
#    https://github.com/giantswarm/devctl/blob/3a85a089d2be9c043c903b21ecc2b63226d07627/pkg/gen/input/makefile/internal/file/Makefile.gen.chainsaw.mk.template
#

SHELL:=/usr/bin/env bash

# Kind cluster name to use
KIND_CLUSTER_NAME ?= chainsaw-kyverno-cluster

# Defaults for local runs; the outer environment / CircleCI environment config overrides them.
# `VAR: value` is a make *rule*, not an assignment, so these have to be `?=` to be usable
# as $(KUBERNETES_VERSION) / $(KYVERNO_VERSION) below.
# repository: kindest/node
KUBERNETES_VERSION ?= v1.33.7
# repository: giantswarm/kyverno-crds
KYVERNO_VERSION ?= v1.17.0
KYVERNO_POLICIES_APP_NAME ?= "kyverno-policies"

##@ Test

.PHONY: kind-create
kind-create: ## create kind cluster if needed
	kind create cluster --name="${KIND_CLUSTER_NAME}" --image="kindest/node:${KUBERNETES_VERSION}"

.PHONY: install-kyverno
install-kyverno:
	# Install Kyverno, enable PolicyExceptions, allowed in all namespaces so tests can use them
	curl -sL https://github.com/kyverno/kyverno/releases/download/$(KYVERNO_VERSION)/install.yaml \
		| sed -E 's/^([[:space:]]*)- --enablePolicyException=false$$/\1- --enablePolicyException=true\n\1- --exceptionNamespace=*/' \
		| kubectl create -f -
	# Sometimes the next check executes faster than the deployment show up for the Kube API Server, so we need to wait for a second
	sleep 5
	kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kyverno -l app.kubernetes.io/component=admission-controller -n kyverno --timeout 300s

.PHONY: install-policies
install-policies:
	touch tests/chainsaw/values.yaml
	helm upgrade --install $(KYVERNO_POLICIES_APP_NAME) ./helm/$(KYVERNO_POLICIES_APP_NAME) --values ./tests/chainsaw/values.yaml

.PHONY: install-extras
install-extras:
	hack/chainsaw-extra-resources.sh

.PHONY: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONY: dabs
dabs: generate
	dabs.sh --generate-metadata --chart-dir helm/kyverno-policies
