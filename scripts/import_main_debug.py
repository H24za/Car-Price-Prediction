import importlib
import traceback
import sys
from pathlib import Path

out = 'scripts/main_import_trace.txt'
# ensure project root is on sys.path so 'main' can be imported when running from scripts/
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    importlib.import_module('main')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('main imported OK')
except Exception:
    tb = traceback.format_exc()
    with open(out, 'w', encoding='utf-8') as f:
        f.write(tb)
    # also print short message for terminal
    print('Import failed — traceback written to', out)
    raise
