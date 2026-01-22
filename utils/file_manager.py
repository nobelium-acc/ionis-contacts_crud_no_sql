import json
import csv
from pathlib import Path
from xml.etree.ElementTree import indent

from bson import json_util

BASE_EXPORT_DIR = Path("data/export")
BASE_EXPORT_DIR.mkdir(exist_ok=True)

BASE_IMPORT_DIR = Path("data/import")
BASE_IMPORT_DIR.mkdir(exist_ok=True)

def export_json(data, filename):
    """
    Export a list of dicts to a JSON file
    """
    filepath = BASE_EXPORT_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
       f.write(json_util.dumps(data, indent=4))
       # json.dump(data, f, ensure_ascii=False, indent=4)

    return filepath

def export_csv(data, filename):
    """
    Export a list of dicts to a CSV file
    """
    if not data:
        raise ValueError("No data to export")

    filepath = BASE_EXPORT_DIR / filename

    # Build headers dynamically
    fieldnames = sorted({key for item in data for key in item.keys()})

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return filepath


# Import
def import_json(filename):
    filepath = BASE_IMPORT_DIR / filename

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def import_csv(filename):
    filepath = BASE_IMPORT_DIR / filename

    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))



