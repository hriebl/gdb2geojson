.PHONY: ruff

ruff:
	uv run ruff check --select I --fix
	uv run ruff format
