from pathlib import Path
from shutil      import rmtree

THIS_DIR       = Path(__file__).parent
ROLLOUT_DIR    = THIS_DIR / "rollout"
TOKEEP_DIR     = ROLLOUT_DIR / "tokeep"
TOKEEP_DOC_DIR = TOKEEP_DIR / "doc"

PROJECT_NAME = THIS_DIR.name

prefixdoc = f"{PROJECT_NAME}-"

for p in TOKEEP_DOC_DIR.glob('*'):
    if p.is_dir():
        rmtree(p)

    elif (
        p.suffix[1:] != "tex"
        or
        not p.name.startswith(prefixdoc)
    ):
        p.unlink()
