##@ Checks

.PHONY: render-checks
render-checks: ## Assert the rendered verify-image-signatures policies (needs helm and yq).
	@hack/render-checks.sh
