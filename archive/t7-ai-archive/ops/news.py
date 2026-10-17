"""Fixed personal workflow entry; no credentials or private input bytes."""
import sys,runpy
from pathlib import Path
source=Path('/Users/katherinevonduyke/Documents/Claude/2026-10-11/remote-desktop-commander-plugin-app-6a057d268ebc81919918d37eec718425-5/work/core/ai-ops/runtime/news_check.py')
sys.path.insert(0,str(source.parent))
runpy.run_path(str(source),run_name="__main__")
