#!/bin/bash

echo "Running linters..."
ruff check
pycodestyle . --exclude=venv --max-line-length=120
mypy .
read -p "Press any key to continue"

echo "Running pytest..."
pytest -v --cov=strrange --cov-report=term-missing --cov-fail-under=100 --cov-branch --cov-report=html

open htmlcov/index.html
