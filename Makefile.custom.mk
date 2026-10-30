##@ Checks

.PHONY: render-checks
render-checks: ## Assert the rendered verify-image-signatures policies (needs helm and yq).
	@hack/render-checks.sh

# Runs the render checks as part of `make helm-test` in CI.
helm-test: render-checks

##@ Chainsaw helpers

.PHONY: kyverno-fast-background-scan
kyverno-fast-background-scan: ## Set the Kyverno reports controller to rescan every minute for the chainsaw Audit test.
	kubectl -n kyverno get deployment kyverno-reports-controller -o json \
		| jq '(.spec.template.spec.containers[] | select(.name == "controller") | .args) |= (map(select(startswith("--backgroundScanInterval=") | not)) + ["--backgroundScanInterval=1m"])' \
		| kubectl replace -f -
	kubectl -n kyverno rollout status deployment kyverno-reports-controller --timeout 300s
