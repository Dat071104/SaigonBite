"""Build this state machine from its adjacent JSON using the shared P2 renderer."""
from pathlib import Path
import runpy,sys
sys.dont_write_bytecode=True
renderer=Path(__file__).resolve().parents[1]/"shared/sm_order.py"
runpy.run_path(str(renderer))["build"](Path(__file__).with_suffix(".json"))
