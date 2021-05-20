.PHONY: generate
generate:
	./template.sh

.PHONY: verify
verify:
	@$(MAKE) generate
	git diff --exit-code
