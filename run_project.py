"""Regenerate the committed visuals and research report from outputs/."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT / "create_visuals.py")], check=True, cwd=ROOT)
subprocess.run([sys.executable, str(ROOT / "build_report.py")], check=True, cwd=ROOT)
print("Generated visuals and report successfully.")
