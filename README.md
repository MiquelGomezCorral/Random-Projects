# random

Random small projects and code I create

# Create env

```bash
python3.12 -m venv venv
source venv/bin/activate

pip install uv
uv pip install -r requirements.txt

uv pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```
