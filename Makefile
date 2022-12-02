.EXPORT_ALL_VARIABLES:
VERSION:=$(shell cat VERSION)

all: build

version:
	echo "__version__ = \"${VERSION}\"" > py/pkg/h2o_nitro_plotly/version.py

setup: clean ## Install dependencies
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install --editable .

purge: ## Purge previous build
	rm -rf build dist *.egg-info

.PHONY: build
build: purge ## Build wheel and docs
	./venv/bin/python setup.py bdist_wheel

publish: build ## Publish wheel
	git tag v$(VERSION)
	git push origin && git push origin --tags
	./venv/bin/python -m twine upload dist/*

clean: purge ## Clean everything
	rm -rf venv

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

