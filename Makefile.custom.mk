##@ Chainsaw helpers

.PHONY: kyverno-fast-background-scan
kyverno-fast-background-scan: ## Set the Kyverno reports controller to rescan every minute for the chainsaw Audit test.
	kubectl -n kyverno get deployment kyverno-reports-controller -o json \
		| jq '(.spec.template.spec.containers[] | select(.name == "controller") | .args) |= (map(select(startswith("--backgroundScanInterval=") | not)) + ["--backgroundScanInterval=1m"])' \
		| kubectl replace -f -
	kubectl -n kyverno rollout status deployment kyverno-reports-controller --timeout 300s

.PHONY: ensure-cleanup-rbac
ensure-cleanup-rbac: ## Apply the chart's cleanup-controller ClusterRole first, so the ClusterCleanupPolicy passes the cleanup webhook's permission check.
	helm template kyverno-policies helm/kyverno-policies --values ./tests/chainsaw/values.yaml \
		| yq 'select(.kind == "ClusterRole" and .metadata.name == "kyverno:kyverno-policies:cleanup-policyexceptions")' \
		| kubectl apply -f -
	@for i in $$(seq 1 30); do \
		if kubectl auth can-i delete policyexceptions.policies.kyverno.io --as=system:serviceaccount:kyverno:kyverno-cleanup-controller >/dev/null 2>&1; then exit 0; fi; \
		sleep 2; \
	done; echo "the cleanup controller did not get PolicyException delete permission within 60s" >&2; exit 1

install-policies: ensure-cleanup-rbac
