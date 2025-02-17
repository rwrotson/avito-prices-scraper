graph:  ## Generate dependency graph
	uv run pydeps src/main.py --max-bacon 3 | dot -Tpng -o dependencies_graph.png
	@echo "Graph saved as dependencies_graph.png"

format:  ## Format code
	uv run ruff format --line-length 120
	uv run ruff check --select I --fix
	@echo "Code formatted"
