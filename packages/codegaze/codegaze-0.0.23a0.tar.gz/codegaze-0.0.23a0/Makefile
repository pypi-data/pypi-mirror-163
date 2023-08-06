
node_modules:
	npm install

.PHONY: check
check: pycodestyle pyright test test-coverage

.PHONY: pyright
pyright:
	npx pyright

.PHONY: test
test:
	python3 -m coverage run --rcfile .coveragerc \
		-m pytest

.PHONY: pycodestyle
pycodestyle:
	python3 -m pycodestyle 

.PHONY: test-coverage
test-coverage: test
	@python3 -m coverage report --show-missing --fail-under 95; \
	if [ $$? == 0 ]; then \
		echo "\nFull test coverage"; \
	else \
		echo "\nOne or more files are not fully covered."; \
		echo "Tip Use pragma: no cover on untestable lines"; \
	fi; \
	echo 

.PHONY: docstring-coverage
docstring-coverage:
	python3 -m interrogate -v .

.PHONY: pip-install
pip-install:
	python3 -m pip install .

.PHONY: tree-sitter
tree-sitter:
	python3 scripts/install_treesitter.py

.PHONY: install
install: pip-install tree-sitter node_modules
