# uv Snippets

## Creating a New Project

```bash
uv init my-project
cd my-project
```

Creates `pyproject.toml`, `.python-version`, `README.md`, `main.py`, and a Git repository.

**Variations:**

```bash
uv init                                # Initialize in the current directory
uv init my-project --python=3.13.14    # Pin a Python version
uv init my-project --lib               # Create a library (src/ layout)
```

## Virtual Environments

```bash
uv venv --python=python3.13.14
source .venv/bin/activate
```

## Installing Packages

```bash
uv pip install torch                # Install a single package
uv pip install -r requirements.txt  # Install from a requirements file
uv add jupyterlab                   # Add a dependency to a uv project (updates pyproject.toml + uv.lock)
```

## Jupyter Notebooks

```bash
uv pip install jupyterlab
uv run jupyter lab
```
