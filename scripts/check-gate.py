#!/usr/bin/env python3
"""Exercise the positive fixture and a deliberate assertion failure."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests/firmware-regression.yaml"


def run(script, case, expected_code):
    out = ROOT / "out" / case
    completed = subprocess.run([
        os.environ.get("LABWIRED_CLI", "labwired"), "test", "--script", str(script),
        "--output-dir", str(out), "--no-uart-stdout",
    ], cwd=ROOT, check=False)
    result = json.loads((out / "result.json").read_text())
    expected_status = "pass" if expected_code == 0 else "fail"
    if completed.returncode != expected_code or result.get("status") != expected_status:
        raise SystemExit(f"{case}: expected {expected_status}/exit {expected_code}, got {result.get('status')}/exit {completed.returncode}")
    if not result.get("assertions"):
        raise SystemExit(f"{case}: no behavioral assertions were evaluated")
    if expected_code == 1 and not any(
        a.get("passed") is False and "uart_contains" in a.get("assertion", {})
        for a in result["assertions"]
    ):
        raise SystemExit("negative: the UART assertion did not fail")
    print(f"{case}: expected {expected_status}, exit {completed.returncode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-only", action="store_true")
    args = parser.parse_args()
    if not args.negative_only:
        run(SCRIPT, "positive", 0)
    changed, count = re.subn(
        r"(?m)^(\s*-\s*uart_contains:)\s*.*$",
        r'\1 "LABWIRED_INTENTIONALLY_WRONG_EXPECTATION_32f416d9"',
        SCRIPT.read_text(), count=1,
    )
    if count != 1:
        raise SystemExit("negative control needs a uart_contains assertion")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", dir=SCRIPT.parent, delete=False) as temporary:
        temporary.write(changed)
        path = Path(temporary.name)
    try:
        run(path, "negative", 1)
    finally:
        path.unlink()


if __name__ == "__main__":
    main()
