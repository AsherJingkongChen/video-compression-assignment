from pathlib import Path

ASSETS_DIR_PATH = (Path(__file__) / "../../../../assets").resolve()
OUTPUTS_DIR_PATH = (Path(__file__) / "../../../../outputs").resolve()
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)
