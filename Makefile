.DEFAULT_GOAL := help

.PHONY: build
build:  ## Build site
	rm -rf site
	mkdir site
	python main.py

.PHONY: format
format:  ## Autoformat Python code
	ruff main.py --fix
	black main.py

.PHONY: help
help:
	@printf "\nUsage: make <commands> \n\nAvailable commands:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint:  ## Lint Python code
	black --check main.py
	ruff main.py

.PHONY: lock
lock:  ## Regenerate requirements.txt lock file
	pip-compile requirements.in
