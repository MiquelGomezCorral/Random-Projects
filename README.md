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


# Reduce image size
```
python ./src/images/reduce_quality.py -i /mnt/c/Users/mique/Desktop/SyncMaikol/.Importantes/.Fotos/Fotos/Poland/all -o /mnt/c/Users/mique/Desktop/SyncMaikol/.Importantes/.Fotos/Fotos/Poland/all_reduced/
```