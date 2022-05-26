.PHONY: all

CMD := poetry run

all: pre-commit

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	@poetry install
	$(CMD) pre-commit install
