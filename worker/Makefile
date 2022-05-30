.PHONY: all

CMD := poetry run

TESTS := ./tests

all: install-deps pre-commit test

test: test-unit

test-unit:
	$(CMD) pytest -vv $(TESTS)

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	@poetry install
	$(CMD) pre-commit install

run-server:
	$(CMD) python -m src.main
