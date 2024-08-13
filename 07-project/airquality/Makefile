RUFF = poetry run ruff

# Check for issues without fixing
.PHONY: lint
lint:
	$(RUFF) check

# Fix issues automatically where possible
.PHONY: fix
fix:
	$(RUFF) check --fix

# Format the files
.PHONY: format
format:
	$(RUFF) format