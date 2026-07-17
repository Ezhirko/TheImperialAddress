from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

INTERNAL_FILE = DATA_DIR / "InternalPopulation.xlsx"
OWNER_FILE = DATA_DIR / "OwnersDirectory.xlsx"
MYGATE_FILE = DATA_DIR / "Mygate_resident_details.csv"