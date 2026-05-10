"""Regenerates Pydantic v2 model files from schemas/*.json.

Run after editing any schema file:
    python scripts/regenerate_models.py

Or regenerate just one schema:
    python scripts/regenerate_models.py live_game
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCHEMAS_DIR = Path("baseball_display/mlb_api/schemas")
MODELS_DIR = Path("baseball_display/mlb_api/models")

# Maps schema filename → output Python file in MODELS_DIR
SCHEMA_TO_MODEL: dict[str, str] = {
    "live_game.json": "game.py",
    "schedule.json": "schedule.py",
    "teams.json": "teams.py",
    "roster.json": "roster.py",
    "person.json": "person.py",
    "stats.json": "stats.py",
}

# datamodel-codegen base flags for all schemas
CODEGEN_FLAGS = [
    "--input-file-type",
    "jsonschema",
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--reuse-model",  # collapse identical model structures
    "--use-title-as-name",  # use schema "title" fields as class names
    "--force-optional",  # schemas are inferred from one sample; real responses
    # often omit fields (e.g. pre-game vs in-progress vs final)
]


def regenerate(schema_name: str, model_name: str) -> bool:
    schema_path = SCHEMAS_DIR / schema_name
    output_path = MODELS_DIR / model_name

    if not schema_path.exists():
        print(f"  SKIP {schema_name} — file not found")
        return False

    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input",
        str(schema_path),
        "--output",
        str(output_path),
        *CODEGEN_FLAGS,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr.strip()

    if result.returncode != 0:
        print(f"  ERROR generating {model_name}:")
        print(f"    {stderr[:400]}")
        return False

    size = output_path.stat().st_size
    print(f"  OK  {model_name}  ({size:,} bytes)")
    if stderr:
        # FutureWarnings etc. — print but don't treat as failure
        for line in stderr.splitlines():
            if "warning" in line.lower() or "Warning" in line:
                continue  # suppress known formatter warnings
            print(f"    WARN: {line}")
    return True


def main() -> None:
    # Optional: filter to specific schema names passed as CLI args
    targets: set[str] = set()
    for arg in sys.argv[1:]:
        # Accept either "live_game" or "live_game.json"
        key = arg if arg.endswith(".json") else f"{arg}.json"
        if key in SCHEMA_TO_MODEL:
            targets.add(key)
        else:
            print(f"Unknown schema: {arg!r}  (known: {', '.join(SCHEMA_TO_MODEL)})")
            sys.exit(1)

    to_run = {k: v for k, v in SCHEMA_TO_MODEL.items() if not targets or k in targets}

    ok = 0
    for schema_name, model_name in to_run.items():
        print(f"{schema_name} → {model_name}")
        if regenerate(schema_name, model_name):
            ok += 1

    print(f"\n{ok}/{len(to_run)} models generated successfully.")
    if ok < len(to_run):
        sys.exit(1)


if __name__ == "__main__":
    main()
