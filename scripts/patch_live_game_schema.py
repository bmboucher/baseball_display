"""Adds title fields and $defs/$ref deduplication to mlb_api/schemas/live_game.json.

Away/Home nodes at the same semantic level are replaced with $ref references
to a shared $defs entry so datamodel-codegen generates exactly one class.

Run this after build_schemas.py, then regenerate models:
    python scripts/patch_live_game_schema.py
    python scripts/regenerate_models.py live_game
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

SCHEMA_PATH = Path("baseball_display/mlb_api/schemas/live_game.json")
P = "properties"  # shorthand


def nav(obj: dict, *keys: str) -> dict | None:
    """Navigate nested dicts; return None if any key is missing."""
    for k in keys:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(k)
        if obj is None:
            return None
    return obj


def set_node(schema: dict, value: dict, *path: str) -> None:
    """Replace the dict node at *path with *value in-place."""
    parent = nav(schema, *path[:-1])
    if parent is None:
        print(f"  MISS  set_node {path}")
        return
    parent[path[-1]] = value


def set_title(schema: dict, title: str, *path: str) -> None:
    node = nav(schema, *path)
    if node is None:
        print(f"  MISS  title {title!r} at {path[-3:]}")
        return
    node["title"] = title


def extract_def(schema: dict, name: str, *source_path: str) -> None:
    """Copy the node at source_path into $defs[name] (titled), no-op if already there."""
    if name in schema.setdefault("$defs", {}):
        return
    node = nav(schema, *source_path)
    if node is None:
        print(f"  MISS  extract_def {name!r} from {source_path[-3:]}")
        return
    defn = copy.deepcopy(node)
    defn["title"] = name
    schema["$defs"][name] = defn
    print(f"  DEF   {name!r}")


def ref(name: str) -> dict:
    return {"$ref": f"#/$defs/{name}"}


def dedup(schema: dict, name: str, *paths: tuple[str, ...]) -> None:
    """Extract first path as $defs[name]; replace all paths with $ref."""
    extract_def(schema, name, *paths[0])
    for path in paths:
        set_node(schema, ref(name), *path)
        print(f"  REF   {name!r}  ← {' > '.join(path[-3:])}")


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # 1. Deduplicate Away/Home shared schemas via $defs + $ref
    # ------------------------------------------------------------------

    # gameData.teams — full team record
    dedup(
        schema,
        "GameTeam",
        (P, "gameData", P, "teams", P, "away"),
        (P, "gameData", P, "teams", P, "home"),
    )

    # gameData.review — challenge review counts
    dedup(
        schema,
        "ReviewCounts",
        (P, "gameData", P, "review", P, "away"),
        (P, "gameData", P, "review", P, "home"),
    )

    # gameData.absChallenges — ABS challenge counts
    dedup(
        schema,
        "AbsChallengeCounts",
        (P, "gameData", P, "absChallenges", P, "away"),
        (P, "gameData", P, "absChallenges", P, "home"),
    )

    # gameData.probablePitchers — minimal person stub
    dedup(
        schema,
        "PersonRef",
        (P, "gameData", P, "probablePitchers", P, "away"),
        (P, "gameData", P, "probablePitchers", P, "home"),
    )

    # gameData.moundVisits — mound visit counts
    dedup(
        schema,
        "MoundVisitCounts",
        (P, "gameData", P, "moundVisits", P, "away"),
        (P, "gameData", P, "moundVisits", P, "home"),
    )

    # linescore innings halves + team totals — same shape
    dedup(
        schema,
        "LinescoreInningHalf",
        (P, "liveData", P, "linescore", P, "innings", "items", P, "away"),
        (P, "liveData", P, "linescore", P, "innings", "items", P, "home"),
        (P, "liveData", P, "linescore", P, "teams", P, "away"),
        (P, "liveData", P, "linescore", P, "teams", P, "home"),
    )

    # ------------------------------------------------------------------
    # 2. Boxscore team stat blocks — MUST run before BoxscoreTeam dedup
    #    and innermost before outermost
    # ------------------------------------------------------------------

    # Team batting/pitching/fielding sub-objects
    dedup(
        schema,
        "TeamBattingStats",
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "away",
            P,
            "teamStats",
            P,
            "batting",
        ),
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "home",
            P,
            "teamStats",
            P,
            "batting",
        ),
    )
    dedup(
        schema,
        "TeamPitchingStats",
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "away",
            P,
            "teamStats",
            P,
            "pitching",
        ),
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "home",
            P,
            "teamStats",
            P,
            "pitching",
        ),
    )
    dedup(
        schema,
        "TeamFieldingStats",
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "away",
            P,
            "teamStats",
            P,
            "fielding",
        ),
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "teams",
            P,
            "home",
            P,
            "teamStats",
            P,
            "fielding",
        ),
    )

    # Team stats wrapper (batting/pitching/fielding are now $refs)
    dedup(
        schema,
        "TeamStats",
        (P, "liveData", P, "boxscore", P, "teams", P, "away", P, "teamStats"),
        (P, "liveData", P, "boxscore", P, "teams", P, "home", P, "teamStats"),
    )

    # ------------------------------------------------------------------
    # 3. BoxscorePlayer stat blocks — innermost first, then parent wrapper
    # ------------------------------------------------------------------

    away_player = (
        P,
        "liveData",
        P,
        "boxscore",
        P,
        "teams",
        P,
        "away",
        P,
        "players",
        "additionalProperties",
    )
    home_player = (
        P,
        "liveData",
        P,
        "boxscore",
        P,
        "teams",
        P,
        "home",
        P,
        "players",
        "additionalProperties",
    )
    top_player = (
        P,
        "liveData",
        P,
        "boxscore",
        P,
        "topPerformers",
        "items",
        P,
        "player",
    )

    # Current-game stats: batting/pitching/fielding first, then wrapper
    dedup(
        schema,
        "PlayerBattingStats",
        (*away_player, P, "stats", P, "batting"),
        (*home_player, P, "stats", P, "batting"),
        (*top_player, P, "stats", P, "batting"),
    )
    dedup(
        schema,
        "PlayerPitchingStats",
        (*away_player, P, "stats", P, "pitching"),
        (*home_player, P, "stats", P, "pitching"),
        (*top_player, P, "stats", P, "pitching"),
    )
    dedup(
        schema,
        "PlayerFieldingStats",
        (*away_player, P, "stats", P, "fielding"),
        (*home_player, P, "stats", P, "fielding"),
        (*top_player, P, "stats", P, "fielding"),
    )
    dedup(
        schema,
        "PlayerStats",
        (*away_player, P, "stats"),
        (*home_player, P, "stats"),
        (*top_player, P, "stats"),
    )

    # Season stats: batting/pitching/fielding first, then wrapper
    dedup(
        schema,
        "PlayerSeasonBattingStats",
        (*away_player, P, "seasonStats", P, "batting"),
        (*home_player, P, "seasonStats", P, "batting"),
        (*top_player, P, "seasonStats", P, "batting"),
    )
    dedup(
        schema,
        "PlayerSeasonPitchingStats",
        (*away_player, P, "seasonStats", P, "pitching"),
        (*home_player, P, "seasonStats", P, "pitching"),
        (*top_player, P, "seasonStats", P, "pitching"),
    )
    dedup(
        schema,
        "PlayerSeasonFieldingStats",
        (*away_player, P, "seasonStats", P, "fielding"),
        (*home_player, P, "seasonStats", P, "fielding"),
        (*top_player, P, "seasonStats", P, "fielding"),
    )
    dedup(
        schema,
        "PlayerSeasonStats",
        (*away_player, P, "seasonStats"),
        (*home_player, P, "seasonStats"),
        (*top_player, P, "seasonStats"),
    )

    # BoxscorePlayer value schema (stats/seasonStats are now $refs)
    dedup(schema, "BoxscorePlayer", tuple(away_player), tuple(home_player))

    # BoxscoreTeam (outermost — teamStats and players are now $refs)
    dedup(
        schema,
        "BoxscoreTeam",
        (P, "liveData", P, "boxscore", P, "teams", P, "away"),
        (P, "liveData", P, "boxscore", P, "teams", P, "home"),
    )

    # topPerformers.player: give it a name before sections below navigate it
    set_title(schema, "TopPerformerPlayer", *top_player)

    # ------------------------------------------------------------------
    # 4. plays.allPlays vs plays.currentPlay deduplication
    #    Innermost sub-schemas are extracted BEFORE their parents so that
    #    parent $defs already contain $refs rather than inline duplicates.
    # ------------------------------------------------------------------

    PLAYS = (P, "liveData", P, "plays")
    ALL = (*PLAYS, P, "allPlays", "items")  # one AllPlay item
    CUR = (*PLAYS, P, "currentPlay")

    # 4a. Count — identical at 4 paths (play-level + play-event-level, both sides)
    dedup(
        schema,
        "Count",
        (*ALL, P, "count"),
        (*ALL, P, "playEvents", "items", P, "count"),
        (*CUR, P, "count"),
        (*CUR, P, "playEvents", "items", P, "count"),
    )

    # 4b. Coordinates — 3 genuinely different shapes, context names
    dedup(
        schema,
        "PitchCoordinates",
        (*ALL, P, "playEvents", "items", P, "pitchData", P, "coordinates"),
        (*CUR, P, "playEvents", "items", P, "pitchData", P, "coordinates"),
    )
    dedup(
        schema,
        "HitCoordinates",
        (*ALL, P, "playEvents", "items", P, "hitData", P, "coordinates"),
        (*CUR, P, "playEvents", "items", P, "hitData", P, "coordinates"),
    )
    dedup(
        schema,
        "FieldCoordinates",
        (
            *PLAYS,
            P,
            "playsByInning",
            "items",
            P,
            "hits",
            P,
            "away",
            "items",
            P,
            "coordinates",
        ),
        (
            *PLAYS,
            P,
            "playsByInning",
            "items",
            P,
            "hits",
            P,
            "home",
            "items",
            P,
            "coordinates",
        ),
    )

    # 4c. Breaks (inside PitchData)
    dedup(
        schema,
        "Breaks",
        (*ALL, P, "playEvents", "items", P, "pitchData", P, "breaks"),
        (*CUR, P, "playEvents", "items", P, "pitchData", P, "breaks"),
    )

    # 4d. PitchCall + EventType + StatType — before their parent containers
    dedup(
        schema,
        "PitchCall",
        (*ALL, P, "playEvents", "items", P, "details", P, "call"),
        (*CUR, P, "playEvents", "items", P, "details", P, "call"),
    )
    dedup(
        schema,
        "EventType",
        (*ALL, P, "playEvents", "items", P, "details", P, "type"),
        (*CUR, P, "playEvents", "items", P, "details", P, "type"),
    )
    dedup(
        schema,
        "StatType",
        (
            *ALL,
            P,
            "matchup",
            P,
            "batterHotColdZoneStats",
            P,
            "stats",
            "items",
            P,
            "type",
        ),
        (
            *CUR,
            P,
            "matchup",
            P,
            "batterHotColdZoneStats",
            P,
            "stats",
            "items",
            P,
            "type",
        ),
    )

    # 4e. PitchData + HitData + PlayEventDetails — before PlayEvent
    dedup(
        schema,
        "PitchData",
        (*ALL, P, "playEvents", "items", P, "pitchData"),
        (*CUR, P, "playEvents", "items", P, "pitchData"),
    )
    dedup(
        schema,
        "HitData",
        (*ALL, P, "playEvents", "items", P, "hitData"),
        (*CUR, P, "playEvents", "items", P, "hitData"),
    )
    dedup(
        schema,
        "PlayEventDetails",
        (*ALL, P, "playEvents", "items", P, "details"),
        (*CUR, P, "playEvents", "items", P, "details"),
    )

    # 4f. PlayerIdRef — id+link player stubs — before Runner/PlayEvent consume them
    dedup(
        schema,
        "PlayerIdRef",
        (*ALL, P, "runners", "items", P, "credits", "items", P, "player"),
        (*ALL, P, "playEvents", "items", P, "player"),
        (*CUR, P, "runners", "items", P, "credits", "items", P, "player"),
    )

    # 4g. PlayEvent — now contains $refs for all its inner types
    dedup(
        schema,
        "PlayEvent",
        (*ALL, P, "playEvents", "items"),
        (*CUR, P, "playEvents", "items"),
    )

    # 4h. RunnerDetails + RunnerMovement + FieldingCredit — before Runner
    dedup(
        schema,
        "RunnerDetails",
        (*ALL, P, "runners", "items", P, "details"),
        (*CUR, P, "runners", "items", P, "details"),
    )
    dedup(
        schema,
        "RunnerMovement",
        (*ALL, P, "runners", "items", P, "movement"),
        (*CUR, P, "runners", "items", P, "movement"),
    )
    dedup(
        schema,
        "FieldingCredit",
        (*ALL, P, "runners", "items", P, "credits", "items"),
        (*CUR, P, "runners", "items", P, "credits", "items"),
    )

    # 4i. Runner — movement/details/credits are now $refs
    dedup(
        schema, "Runner", (*ALL, P, "runners", "items"), (*CUR, P, "runners", "items")
    )

    # 4j. Matchup + About + Result
    dedup(schema, "Matchup", (*ALL, P, "matchup"), (*CUR, P, "matchup"))
    dedup(schema, "About", (*ALL, P, "about"), (*CUR, P, "about"))
    dedup(schema, "Result", (*ALL, P, "result"), (*CUR, P, "result"))

    # ------------------------------------------------------------------
    # 5. Context names for genuinely different schemas sharing a key name
    # ------------------------------------------------------------------

    # Status: game-level (abstractGameState etc.) vs player availability (code/description)
    set_title(schema, "GameStatus", P, "gameData", P, "status")
    dedup(
        schema,
        "PlayerStatus",
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "topPerformers",
            "items",
            P,
            "player",
            P,
            "status",
        ),
        ("$defs", "BoxscorePlayer", P, "status"),
    )

    # Teams wrappers — each has different away/home inner types after $ref dedup
    set_title(schema, "GameDataTeams", P, "gameData", P, "teams")
    set_title(schema, "LinescoreTeams", P, "liveData", P, "linescore", P, "teams")
    set_title(schema, "BoxscoreTeams", P, "liveData", P, "boxscore", P, "teams")

    # Team: HitTeam (5 props with springLeague) vs LinescoreTeam (3 props)
    dedup(
        schema,
        "HitTeam",
        (*PLAYS, P, "playsByInning", "items", P, "hits", P, "away", "items", P, "team"),
        (*PLAYS, P, "playsByInning", "items", P, "hits", P, "home", "items", P, "team"),
    )
    # BoxscoreTeam.team (already in $defs) has the same 5-prop shape — reuse HitTeam
    set_node(schema, ref("HitTeam"), "$defs", "BoxscoreTeam", P, "team")
    dedup(
        schema,
        "LinescoreTeam",
        (P, "liveData", P, "linescore", P, "defense", P, "team"),
        (P, "liveData", P, "linescore", P, "offense", P, "team"),
    )

    # Person: TopPerformerPerson has extra boxscoreName vs BoxscorePlayer's person
    set_title(
        schema,
        "TopPerformerPerson",
        P,
        "liveData",
        P,
        "boxscore",
        P,
        "topPerformers",
        "items",
        P,
        "player",
        P,
        "person",
    )
    set_title(schema, "PlayerPerson", "$defs", "BoxscorePlayer", P, "person")

    # Players dicts — RootModel[Dict[str, X]] wrappers for different value types
    set_title(schema, "GameDataPlayersDict", P, "gameData", P, "players")
    set_title(schema, "BoxscorePlayersDict", "$defs", "BoxscoreTeam", P, "players")

    # GameStatus: title on gameData.status would conflict with the auto-name of
    # the 'gameStatus' property on BoxscorePlayer/TopPerformerPlayer → dedup those instead
    set_title(schema, "GameState", P, "gameData", P, "status")
    dedup(
        schema,
        "PlayerGameStatus",
        (
            P,
            "liveData",
            P,
            "boxscore",
            P,
            "topPerformers",
            "items",
            P,
            "player",
            P,
            "gameStatus",
        ),
        ("$defs", "BoxscorePlayer", P, "gameStatus"),
    )

    # Venue: context names for game venue vs team venue
    set_title(schema, "GameVenue", P, "gameData", P, "venue")
    set_title(schema, "TeamVenue", "$defs", "GameTeam", P, "venue")

    # InfoItem: two different shapes inside boxscore.info vs BoxscoreTeam.info
    set_title(
        schema, "BoxscoreInfoItem", P, "liveData", P, "boxscore", P, "info", "items"
    )
    set_title(schema, "TeamInfoItem", "$defs", "BoxscoreTeam", P, "info", "items")

    # OfficialAssignment: title the officials array item so its class name doesn't
    # conflict with the inner 'official' person property (which reuses OfficialScorer)
    set_title(
        schema,
        "OfficialAssignment",
        P,
        "liveData",
        P,
        "boxscore",
        P,
        "officials",
        "items",
    )

    # Runner person inside RunnerDetails: set to PersonRef to avoid conflict with
    # the $defs.Runner class that codegen also names "Runner"
    set_node(schema, ref("PersonRef"), "$defs", "RunnerDetails", P, "runner")

    # HotColdZoneStat: the leaf 'stat' (name+zones) inside splits conflicts with
    # the 'Stat' class from the parent stats array items — title it before Matchup
    # was already deduplicated, so navigate into $defs.Matchup
    set_title(
        schema,
        "HotColdZoneStat",
        "$defs",
        "Matchup",
        P,
        "batterHotColdZoneStats",
        P,
        "stats",
        "items",
        P,
        "splits",
        "items",
        P,
        "stat",
    )

    # ------------------------------------------------------------------
    # 6. Save
    # ------------------------------------------------------------------
    SCHEMA_PATH.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"\nSaved {SCHEMA_PATH} ({SCHEMA_PATH.stat().st_size:,} bytes)")
    defs = list(schema.get("$defs", {}).keys())
    print(f"{len(defs)} $defs: {defs}")


if __name__ == "__main__":
    main()
