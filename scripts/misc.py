from scripts.archive import load_config
from os import scandir, remove

def clean_archive():
    config = load_config()
    with scandir(config['zip_path']) as archives:
        for archive in archives:
            if not archive.name.startswith('.') and archive.is_file():
                remove(archive.path)