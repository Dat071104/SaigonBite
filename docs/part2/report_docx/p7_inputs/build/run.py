# Runs a P7 build script with the vendored deps on sys.path (miniconda Python 3.13 provides python-docx).
# Usage: python run.py <script.py> [...]
import sys, runpy
sys.path.insert(0, r'D:\RAD\FINAL\Part2\build\p7_latex\deps')
for script in sys.argv[1:]:
    print('==', script, flush=True)
    runpy.run_path(script, run_name='__main__')
