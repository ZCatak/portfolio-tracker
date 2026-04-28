# Portfolio Tracker

A small command-line application for tracking an investment portfolio.

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) for dependency management

Install uv if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Getting started

Clone the repository and move into the project folder:

```bash
git clone https://github.com/ZCatak/portfolio-tracker
cd portfolio-tracker
```

Install the project dependencies. This command reads the `pyproject.toml` and `uv.lock` files to create a local virtual environment (`.venv/`) with the exact package versions used during development:

```bash
uv sync
```

Run the application:

```bash
uv run python main.py
```
