from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
shutil.rmtree(root/'reports'/'generated',ignore_errors=True)
for path in root.rglob('__pycache__'): shutil.rmtree(path,ignore_errors=True)
print('PASS capstone clean')
