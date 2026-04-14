from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_step(script_name: str) -> None:
    script_path = PROJECT_ROOT / "src" / script_name
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(PROJECT_ROOT), check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {script_name}")


def main() -> None:
    print("[1/2] Generating sample security events...")
    run_step("generate_sample_logs.py")

    print("[2/2] Running alert detection rules...")
    run_step("detect_alerts.py")

    print("Pipeline finished successfully.")
    print("Check output/alerts.csv and output/alerts_report.md")


if __name__ == "__main__":
    main()
