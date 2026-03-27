import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

src_path = str(SRC_DIR)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
