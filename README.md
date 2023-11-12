# linked-data-sandbox
Sandbox for experimenting with Linked Data

## Set up the local Python environment

```bash
# Setup the Python version
pyenv install --skip-existing $(cat .python-version)

# Setup the virtual environment
python -m venv .venv --prompt ld-sandbox-py$(cat .python-version)
source .venv/bin/activate

# Install Berkeley DB
brew install berkeley-db@4
BERKELEYDB_DIR=$(brew --prefix berkeley-db@4) pip install berkeleydb==18.1.8

# Install the remaining dependencies
pip install -r requirements.txt
```
