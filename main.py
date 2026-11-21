import os
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out.mkdir(parents=True, exist_ok=True)
shutil.copyfile(root / "assets" / "entry.png", out / "entry.png")
