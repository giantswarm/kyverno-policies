##@ Checks

.PHONY: render-checks
render-checks: ## Assert the rendered verify-image-signatures policies (needs helm and yq).
	@hack/render-checks.sh

# The chart-tests workflow runs `make helm-test`; this prerequisite makes it run
# the render checks too.
helm-test: render-checks

##@ Chainsaw helpers

.PHONY: kyverno-fast-background-scan
kyverno-fast-background-scan: ## Make the Kyverno reports controller rescan every minute (upstream: hourly) so chainsaw can assert background-scan PolicyReports.
	kubectl -n kyverno get deployment kyverno-reports-controller -o json \
		| jq '(.spec.template.spec.containers[] | select(.name == "controller") | .args) |= (map(select(startswith("--backgroundScanInterval=") | not)) + ["--backgroundScanInterval=1m"])' \
		| kubectl replace -f -
	kubectl -n kyverno rollout status deployment kyverno-reports-controller --timeout 300s
