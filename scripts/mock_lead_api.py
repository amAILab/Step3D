#!/usr/bin/env python3
"""Local mock Step3D lead API.

Reads JSON from stdin or --sample, validates/routes it, optionally writes JSONL log,
and returns the same response shape expected from production backend.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "lead_router.py"


def run_router(raw: str, sample: bool, write_log: bool) -> dict:
    cmd = [sys.executable, str(ROUTER), "--json"]
    if sample:
        cmd.append("--sample")
    if write_log:
        cmd.append("--write-log")
    proc = subprocess.run(cmd, input=None if sample else raw, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        return {"ok": False, "error": (proc.stdout or proc.stderr).strip()}
    result = json.loads(proc.stdout)
    return {
        "ok": True,
        "id": result["projectId"],
        "projectId": result["projectId"],
        "status": result.get("status", "created"),
        "nextStep": result.get("nextStep", "проверить вводные"),
        "transport": "mock-local",
        "logPath": result.get("log_path", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--write-log", action="store_true")
    args = parser.parse_args()
    raw = "" if args.sample else sys.stdin.read()
    print(json.dumps(run_router(raw, args.sample, args.write_log), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
