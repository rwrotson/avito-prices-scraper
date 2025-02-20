graph:  ## Generate dependency graph
	uv run pydeps src/main.py --max-bacon 3 --no-show -T svg -o meta/deps_graph.svg
	@echo "Graph saved as meta/deps_graph.png and meta/deps_graph.svg"

format:  ## Format code
	uv run ruff format --line-length 120
	uv run ruff check --select I --fix
	@echo "Code formatted"
