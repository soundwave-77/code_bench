lint:
	black . && isort . && flake8 . && pylint . && mypy .