##@ Chainsaw helpers

.PHONY: kyverno-fast-background-scan
kyverno-fast-background-scan: ## Set the Kyverno reports controller to rescan every minute for the chainsaw Audit test.
	kubectl -n kyverno get deployment kyverno-reports-controller -o json \
		| jq '(.spec.template.spec.containers[] | select(.name == "controller") | .args) |= (map(select(startswith("--backgroundScanInterval=") | not)) + ["--backgroundScanInterval=1m"])' \
		| kubectl replace -f -
	kubectl -n kyverno rollout status deployment kyverno-reports-controller --timeout 300s
