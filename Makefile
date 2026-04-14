# Hierdurch ist es auf Mac möglich, einfach "make lint" zu schreiben und damit den gegebenen Befehl auszuführen
# ruff check mit automatischer Korrektur
lint:
	uvx ruff check --fix src tests

# ruff Formatierung
format:
	uvx ruff format src tests

security:
	uv audit --no-dev || true
	uv tree --outdated --all-groups --depth=1
