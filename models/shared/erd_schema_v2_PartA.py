"""Regenerate ERD Figure 4.3.1A. Author: 722I0004 · AI-assisted (Codex)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from erd_schema_v2 import build_part

if __name__ == "__main__":
    print(build_part("PartA"))
