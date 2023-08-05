init:
	pip install ".[dev]"

clean:
	rm -rf dist build *.egg-info

build:
	pip install build
	python -m build

publish:
	pip install twine
	python -m twine upload dist/*

test:
	pytest

lint: lint-black lint-flake8 lint-isort

lint-black:
	black --diff --quiet .

lint-flake8:
	flake8

lint-isort:
	isort --diff --quiet .
