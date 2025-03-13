# textbook-marketplace

dimentions of img:
240 * 312
324 * 420


Quick manual:

1) `git clone https://github.com/Second-Book/textbook-marketplace-backend.git`
2) `cd textbook-marketplace-backend`
3) `curl -LsSf https://astral.sh/uv/install.sh | sh` for Linux
4) `export PATH="$HOME/.local/bin:$PATH"` for Linux
5) `uv venv --python 3.12` (it will create .venv)
6) `source .venv/bin/activate` for Linux
7) `uv pip install -r pyproject.toml`
8) `uv run python textbook_marketplace/manage.py migrate`
To start server:
1) Setup database
2) `uv run python textbook_marketplace/manage.py runserver`
