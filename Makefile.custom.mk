.PHONY: generate
generate:
	./template.sh

.PHONY: verify
verify:
	@$(MAKE) generate
	git diff --exit-code

.PHONY: local-setup
local-setup:
	@$(MAKE) generate
	./setup.sh
