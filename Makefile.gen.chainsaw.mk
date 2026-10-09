# DO NOT EDIT. Generated with:
#
#    devctl
#
#    https://github.com/giantswarm/devctl/blob/9c16edd66acf3373af93a22f40cdc6f5780c0486/pkg/gen/input/makefile/internal/file/Makefile.gen.chainsaw.mk.template
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
# The chart to install and build: helm/$(KYVERNO_POLICIES_APP_NAME) when that is set and has a
# Chart.yaml (as in CI), otherwise the one directory under helm/ with a Chart.yaml.
# KYVERNO_POLICIES_APP_NAME only counts here when set before this file is included (env, command
# line or Makefile.custom.mk). Set KYVERNO_POLICIES_CHART_DIR if neither picks the right chart.
ifneq ($(origin KYVERNO_POLICIES_APP_NAME),undefined)
KYVERNO_POLICIES_APP_CHART := $(patsubst %/Chart.yaml,%,$(wildcard helm/$(KYVERNO_POLICIES_APP_NAME)/Chart.yaml))
endif
KYVERNO_POLICIES_CHART_DIR ?= $(or $(KYVERNO_POLICIES_APP_CHART),$(patsubst %/Chart.yaml,%,$(wildcard helm/*/Chart.yaml)))
# The Helm release name. CI sets it to the repository name.
KYVERNO_POLICIES_APP_NAME ?= $(notdir $(patsubst %/,%,$(KYVERNO_POLICIES_CHART_DIR)))

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
install-policies: check-kyverno-policies-chart
	touch tests/chainsaw/values.yaml
	helm upgrade --install $(KYVERNO_POLICIES_APP_NAME) $(KYVERNO_POLICIES_CHART_DIR) --values ./tests/chainsaw/values.yaml

.PHONY: install-extras
install-extras:
	hack/chainsaw-extra-resources.sh

.PHONY: kind-get-kubeconfig
kind-get-kubeconfig:
	kind get kubeconfig --name $(KIND_CLUSTER_NAME) > $(PWD)/kube.config

.PHONY: dabs
dabs: check-kyverno-policies-chart generate
	dabs.sh --generate-metadata --chart-dir $(KYVERNO_POLICIES_CHART_DIR)

.PHONY: check-kyverno-policies-chart
check-kyverno-policies-chart:
	@if [ "$(words $(KYVERNO_POLICIES_CHART_DIR))" != "1" ] || [ ! -f "$(KYVERNO_POLICIES_CHART_DIR)/Chart.yaml" ]; then \
		echo "expected one chart directory with a Chart.yaml, KYVERNO_POLICIES_CHART_DIR is '$(KYVERNO_POLICIES_CHART_DIR)'. Set it to the chart directory." >&2; \
		exit 1; \
	fi
