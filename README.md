# linked-data-sandbox
Sandbox for experimenting with Linked Data

## Set up the local Python environment

```bash
# Setup the Python version
pyenv install --skip-existing $(cat .python-version)

# Setup the virtual environment
python -m venv .venv --prompt ld-sandbox-py$(cat .python-version)
source .venv/bin/activate
pip install -r requirements.txt
```
