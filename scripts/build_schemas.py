"""Fetches MLB API sample responses and generates cleaned JSON schemas.

The key transformation applied automatically:

  gameData.players        ─┐
  boxscore.home.players   ─┤  keyed by "ID####" → patched to
  boxscore.away.players   ─┘  {type: object, additionalProperties: <Player>}

  All player objects at each location are merged by genson into ONE schema so
  datamodel-codegen emits a single Player/BoxscorePlayer class instead of one
  class per player (Batting2, Batting3 ... Batting75, etc.).

Edit mlb_api/schemas/*.json as needed, then run:
    python scripts/regenerate_models.py
"""

from __future__ import annotations

import copy
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

from genson import SchemaBuilder

BASE_URL = "https://statsapi.mlb.com"
UA = "baseball-display/1.0"
SCHEMAS_DIR = Path("baseball_display/mlb_api/schemas")
GAME_PK = 824851  # completed game used as reference


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def merged_schema(*objects: dict) -> dict:
    """Feed multiple JSON objects into genson and return the merged schema."""
    b = SchemaBuilder()
    for obj in objects:
        b.add_object(obj)
    return b.to_schema()


def _nav(obj: Any, *keys: str) -> Any | None:
    """Safe nested dict navigation; returns None if any key is missing."""
    for k in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(k)
    return obj


def _id_keyed(props: dict) -> bool:
    """Return True when all property keys look like MLB player IDs (ID####)."""
    return bool(props) and all(re.match(r"^ID\d+$", k) for k in props)


# ---------------------------------------------------------------------------
# Schema patching
# ---------------------------------------------------------------------------


def _inject_addl_props(schema_node: dict, objects: list[dict], title: str) -> None:
    """Replace an ID-keyed object schema node with additionalProperties."""
    value_schema = merged_schema(*objects)
    value_schema["title"] = title
    schema_node.clear()
    schema_node.update(
        {
            "type": "object",
            "title": "Players",
            "additionalProperties": value_schema,
        }
    )


def patch_game_feed(data: dict, schema: dict) -> dict:
    """Patch all player-dict locations in the live game feed schema."""
    schema = copy.deepcopy(schema)

    patches = [
        # (path to schema node,  path to data values)
        (
            ["properties", "gameData", "properties", "players"],
            ["gameData", "players"],
            "GameDataPlayer",
        ),
        (
            [
                "properties",
                "liveData",
                "properties",
                "boxscore",
                "properties",
                "teams",
                "properties",
                "home",
                "properties",
                "players",
            ],
            ["liveData", "boxscore", "teams", "home", "players"],
            "BoxscorePlayer",
        ),
        (
            [
                "properties",
                "liveData",
                "properties",
                "boxscore",
                "properties",
                "teams",
                "properties",
                "away",
                "properties",
                "players",
            ],
            ["liveData", "boxscore", "teams", "away", "players"],
            "BoxscorePlayer",  # same title → codegen reuses the class
        ),
    ]

    for schema_path, data_path, title in patches:
        # navigate schema
        node = schema
        for k in schema_path[:-1]:
            node = node.get(k, {})
        leaf_key = schema_path[-1]
        if leaf_key not in node:
            print(f"  SKIP patch: schema path {schema_path} not found")
            continue

        # navigate data
        player_dict = _nav(data, *data_path)
        if not isinstance(player_dict, dict) or not player_dict:
            print(f"  SKIP patch: data path {data_path} empty")
            continue

        props = node[leaf_key].get("properties", {})
        if not _id_keyed(props):
            print(f"  SKIP patch: {leaf_key} does not look ID-keyed")
            continue

        _inject_addl_props(node[leaf_key], list(player_dict.values()), title)
        print(
            f"  Patched {leaf_key} ({len(player_dict)} players -> additionalProperties:{title})"
        )

    return schema


# ---------------------------------------------------------------------------
# Per-endpoint builders
# ---------------------------------------------------------------------------


def build_game_feed_schema() -> dict:
    print(f"Fetching live game {GAME_PK}...")
    data = fetch(f"{BASE_URL}/api/v1.1/game/{GAME_PK}/feed/live")
    print("  Building base schema with genson...")
    b = SchemaBuilder()
    b.add_object(data)
    schema = b.to_schema()
    schema["title"] = "GameFeed"
    print("  Patching player dicts...")
    schema = patch_game_feed(data, schema)
    return schema


ENDPOINT_SCHEMAS: dict[str, tuple[str, str]] = {
    # name: (url, root title)
    "schedule": (
        f"{BASE_URL}/api/v1/schedule"
        "?date=2026-05-03&sportId=1&hydrate=team,linescore,flags,review",
        "ScheduleResponse",
    ),
    "teams": (
        f"{BASE_URL}/api/v1/teams?sportId=1",
        "TeamsResponse",
    ),
    "roster": (
        f"{BASE_URL}/api/v1/teams/111/roster/active"
        "?hydrate=person(fullName,primaryNumber,primaryPosition)",
        "RosterResponse",
    ),
    "person": (
        f"{BASE_URL}/api/v1/people/660271?hydrate=currentTeam",
        "PersonResponse",
    ),
    "stats": (
        f"{BASE_URL}/api/v1/people/660271/stats?stats=career&group=hitting",
        "StatsResponse",
    ),
}


def build_simple_schema(url: str, title: str) -> dict:
    print(f"  Fetching {url.split('?')[0].split('/')[-1]}...")
    data = fetch(url)
    b = SchemaBuilder()
    b.add_object(data)
    schema = b.to_schema()
    schema["title"] = title
    return schema


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    SCHEMAS_DIR.mkdir(exist_ok=True)

    # Live game feed
    print("=== live_game ===")
    schema = build_game_feed_schema()
    out = SCHEMAS_DIR / "live_game.json"
    out.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"  Wrote {out} ({out.stat().st_size:,} bytes)")

    # Simple endpoints
    for name, (url, title) in ENDPOINT_SCHEMAS.items():
        print(f"=== {name} ===")
        schema = build_simple_schema(url, title)
        out = SCHEMAS_DIR / f"{name}.json"
        out.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        print(f"  Wrote {out} ({out.stat().st_size:,} bytes)")

    print("\nSchemas written to baseball_display/mlb_api/schemas/")
    print("Edit them if needed, then regenerate models:")
    print("  python scripts/regenerate_models.py")


if __name__ == "__main__":
    main()
