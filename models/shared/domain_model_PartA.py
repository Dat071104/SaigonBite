"""Regenerate the domain_model package, including Part A. Author: 722I0004 · AI-assisted (Codex)."""
import sys,runpy
from pathlib import Path
sys.dont_write_bytecode=True
runpy.run_path(str(Path(__file__).with_name('domain_model.py')),run_name='__main__')
