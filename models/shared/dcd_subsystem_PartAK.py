"""Author: 722I0004 · AI-assisted (Codex). Re-render this shared-model projection."""
from pathlib import Path
import runpy, sys
sys.dont_write_bytecode = True
if __name__ == "__main__":
    coordinator = Path(__file__).with_name("dcd_subsystem.py")
    sys.argv = [str(coordinator), str(Path(__file__).with_suffix(".json"))]
    runpy.run_path(str(coordinator), run_name="__main__")
