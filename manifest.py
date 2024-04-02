import json
import os


def get_latest_manifest(manifest_dir: str = "clubs/manifests"):
    latest = max(os.listdir(manifest_dir))
    with open(f"clubs/manifests/{latest}") as f_:
        return json.load(f_)
