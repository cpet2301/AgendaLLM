# Agenda LLM

## Development Setup

### 1. Install Poetry

Install the Poetry build tool & package manager by following [these instructions](https://python-poetry.org/docs/#installing-with-the-official-installer).

### 2. Clone the Repository

If you're working on this project, you should know how to do this.

### 3. Initialize the Poetry environment

Poetry works a bit differently than `venv` and `pip`. Since the project is already configured, all you need to do is navigate to the root of the repository and do

```bash
poetry init
```

and at this point you're ready to use the virtual environment.

---

## Using the Poetry environment

Rather than sourcing an `activate` script in a `venv` directory, you prefix your commands with `poetry run` and it will automatically run them in the virtual environment poetry made and manages for you.

For example, instead of

```bash
source venv/bin/activate
python3 main.py
```

you would just do

```bash
poetry run python3 main.py
```

### Adding Packages

To add a new package to the repository, simply run

```bash
poetry add <package-name>
```
