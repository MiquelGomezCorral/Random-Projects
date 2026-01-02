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

# Copy photos (backup)

Copy the photos from any device / folder to somewhere else. Use it for backups or anything.


### How to use
> -i input folder
> -o output folder
> -r wether or not to recursively fetch all the input subfolders (default True)
> -d limit date: will only copy file from this date forwards
```bash
source venv/bin/activate

python files/copy_photos_date.py -i "/run/user/1000/gvfs/mtp:host=Xiaomi_POCO_X4_Pro_5G_81290626fe9f/Almacenamiento interno compartido/DCI
M/Camera" -o "/media/turbotowerlnx/TOSHIBA EXT/Miquel/Fotos 2025-09-14 -- 2026-01-02/Fotos" -d "2025-09-15"
```