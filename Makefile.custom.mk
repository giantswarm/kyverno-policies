.PHONY: generate
generate:
	./hack/template.sh

.PHONY: verify
verify:
	@$(MAKE) generate
	git diff --exit-code

.PHONY: clean
clean:
	./hack/cleanup-local.sh

.PHONY: setup
setup:
	@$(MAKE) generate
	./hack/setup-local.sh
