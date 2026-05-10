import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Optional

import pygame
from pydantic import BaseModel, Field
from pygame.event import Event

from baseball_display.constants import PITCH_TYPE_NAMES
from baseball_display.display_constants import (
    LINEUP_NAME_MAX_CHARS,
    MAIN_MENU_ITEMS,
    MENU_NUM_ROWS,
    SETTINGS_MENU_REFRESH_RATE_OPTIONS as REFRESH_RATE_OPTIONS,
    SETTINGS_MENU_ROWS as SETTINGS_ROWS,
    TAB_STATUSES,
    TABS,
)
from baseball_display.mlb_api.models.game import (
    AllPlay,
    BoxscorePlayer,
    GameDataPlayer,
    GameFeed,
)
from baseball_display.settings import get_settings, set_refresh_rate
from baseball_display.statsapi import (
    RosterEntry,
    ScheduledGame,
    TeamInfo,
    get_available_games,
    get_live_game,
    get_player_stats,
    get_roster,
    get_teams,
)

logger = logging.getLogger(__name__)


class HittingStats(BaseModel, frozen=True):
    """Season or career hitting stats, pre-formatted for display."""

    g: str
    avg: str
    obp: str
    slg: str
    ops: str
    hr: str
    rbi: str
    r: str
    sb: str


class PitchingStats(BaseModel, frozen=True):
    """Season or career pitching stats, pre-formatted for display."""

    era: str
    whip: str
    w: str
    l: str
    g: str
    gs: str
    ip: str
    so: str
    bb: str
    h: str
    r: str
    er: str
    hr: str
    pc_st: str  # formatted as "pitches-strikes"


def _build_hitting_stats(raw: dict[str, Any]) -> HittingStats:
    def s(key: str) -> str:
        val = raw.get(key)
        if val is None:
            return "-"
        if isinstance(val, float):
            return f"{val:.3f}"
        return str(val)

    return HittingStats(
        g=s("gamesPlayed"),
        avg=s("avg"),
        obp=s("obp"),
        slg=s("slg"),
        ops=s("ops"),
        hr=s("homeRuns"),
        rbi=s("rbi"),
        r=s("runs"),
        sb=s("stolenBases"),
    )


def _build_pitching_stats(raw: dict[str, Any]) -> PitchingStats:
    def s(key: str) -> str:
        val = raw.get(key)
        if val is None:
            return "-"
        if isinstance(val, float):
            return f"{val:.2f}"
        return str(val)

    pitches = s("numberOfPitches")
    strikes = s("strikes")
    pc_st = f"{pitches}-{strikes}" if pitches != "-" and strikes != "-" else "-"

    return PitchingStats(
        era=s("era"),
        whip=s("whip"),
        w=s("wins"),
        l=s("losses"),
        g=s("gamesPitched"),
        gs=s("gamesStarted"),
        ip=s("inningsPitched"),
        so=s("strikeOuts"),
        bb=s("baseOnBalls"),
        h=s("hits"),
        r=s("runs"),
        er=s("earnedRuns"),
        hr=s("homeRuns"),
        pc_st=pc_st,
    )


class PAEvent(BaseModel, frozen=True):
    """A single event in the current plate appearance, pre-formatted for display."""

    text: str
    category: str  # "ball" | "strike" | "in_play" | "run" | "advance"
    right_text: str | None = None  # right-aligned outcome text for pitch rows


class LineupEntry(BaseModel, frozen=True):
    """One batting-order slot, pre-formatted for display."""

    last_name: str
    number: str
    mlb_id: int
    is_active: bool


class BatterInfo(BaseModel, frozen=True):
    """Current batter identity and today's box-score stats, pre-formatted for display."""

    display_name: str  # "LAST, F."
    number: str
    ab: str
    h: str
    r: str
    rbi: str
    bb: str
    so: str


class PitcherInfo(BaseModel, frozen=True):
    """Current pitcher identity and today's box-score stats, pre-formatted for display."""

    display_name: str  # "FIRST LAST"
    number: str
    ip: str
    h: str
    r: str
    er: str
    so: str
    bb: str
    p: str
    s: str
    wls: str
    era: str
    whip: str


def _fmt_stat(val: Any) -> str:
    """Format a box-score stat for display; None → '-', floats to 2 dp."""
    if val is None:
        return "-"
    if isinstance(val, float):
        return f"{val:.2f}"
    return str(val)


def _strip_hour_zero(s: str) -> str:
    """Replace a leading '0' with a space so '09:05' becomes ' 9:05'."""
    return (" " + s[1:]) if s.startswith("0") else s


def _default_runner_name_map() -> dict[int, str]:
    return {}

def _default_runner_number_map() -> dict[int, str]:
    return {}


def _default_base_segment_list() -> list[tuple[str, str]]:
    return []


def _default_runner_animation_moves() -> list["RunnerAnimationMove"]:
    return []


def _default_lineup_slots() -> dict[int, int]:
    return {}


def _default_infield_slots() -> dict[str, int]:
    return {}


def _default_outfield_slots() -> dict[str, int]:
    return {}

class RunnerAnimationMove(BaseModel, frozen=True):
    player_id: int
    last_name: str
    start_base: str
    end_base: str | None
    is_out: bool = False
    play_index: int


# ---------------------------------------------------------------------------
# Thin wrapper types that replace the baseball package's object graph
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _PitchEvent:
    description: str
    pitch_type_code: str
    speed: float | None
    px: float | None
    pz: float | None
    hit_x: float | None
    hit_y: float | None


@dataclass(frozen=True)
class _RunnerEvent:
    player_id: int | None
    last_name: str
    event_type: str | None
    play_index: int | None
    is_scoring: bool
    is_out: bool
    start_base: str | None
    end_base: str | None
    out_base: str | None
    run_description: str


@dataclass(frozen=True)
class _SubEvent:
    in_player_id: int | None
    in_last_name: str
    out_last_name: str
    out_player_id: int | None


@dataclass(frozen=True)
class _SwitchEvent:
    in_player_id: int | None
    last_name: str
    new_position: str


@dataclass(frozen=True)
class _PickoffEvent:
    description: str
    target_base: str
    is_out: bool


@dataclass
class _Appearance:
    batter_id: int
    batter_last_name: str
    pitcher_id: int
    pa_summary: str
    pa_event_type: str
    is_error: bool
    scoring_runner_count: int
    inning_outs: int
    end_time_str: str | None
    events: list[
        Any
    ]  # list of _PitchEvent | _RunnerEvent | _SubEvent | _SwitchEvent | _PickoffEvent


@dataclass
class _HalfInning:
    appearances: list[_Appearance] = field(default_factory=list)  # type: ignore[assignment]


@dataclass
class _GameData:
    innings: list[tuple[_HalfInning, _HalfInning]]
    away_batting_order: list[int]
    home_batting_order: list[int]
    away_starting_lineup_slots: dict[int, int]
    home_starting_lineup_slots: dict[int, int]
    away_starting_infield_slots: dict[str, int]
    home_starting_infield_slots: dict[str, int]
    away_starting_outfield_slots: dict[str, int]
    home_starting_outfield_slots: dict[str, int]
    away_starting_catcher_id: int | None
    home_starting_catcher_id: int | None
    away_players: dict[str, BoxscorePlayer]
    home_players: dict[str, BoxscorePlayer]
    game_data_players: dict[str, GameDataPlayer]
    winner_id: int | None
    loser_id: int | None


def _parse_batting_order_slot(raw: str | int | None) -> int | None:
    if raw is None:
        return None
    try:
        val = int(raw)
    except (TypeError, ValueError):
        return None
    if val < 100 or val > 900 or val % 100 != 0:
        return None
    return val // 100


def _extract_starting_lineup_slots(
    players: dict[str, BoxscorePlayer],
) -> dict[int, int]:
    slots: dict[int, int] = {}
    for p in players.values():
        if p.person is None or p.person.id is None:
            continue
        slot = _parse_batting_order_slot(p.battingOrder)
        if slot is None:
            continue
        if slot in slots and slots[slot] != p.person.id:
            logger.warning(
                "Duplicate batting-order slot %s: keeping %s, ignoring %s",
                slot,
                slots[slot],
                p.person.id,
            )
            continue
        slots[slot] = p.person.id
    return slots


def _fill_lineup_slots_from_order(
    slots: dict[int, int],
    batting_order: list[int],
) -> dict[int, int]:
    out = dict(slots)
    for idx, pid in enumerate(batting_order[:9], start=1):
        out.setdefault(idx, pid)
    return out


def _normalize_defense_slot(pos: str | None) -> str | None:
    if pos is None:
        return None
    key = pos.strip().lower()
    mapping: dict[str, str] = {
        "1b": "1b",
        "first": "1b",
        "2b": "2b",
        "second": "2b",
        "3b": "3b",
        "third": "3b",
        "ss": "ss",
        "shortstop": "ss",
        "lf": "lf",
        "left": "lf",
        "left field": "lf",
        "cf": "cf",
        "center": "cf",
        "center field": "cf",
        "rf": "rf",
        "right": "rf",
        "right field": "rf",
        "c": "c",
        "catcher": "c",
    }
    return mapping.get(key)


def _normalize_infield_slot(pos: str | None) -> str | None:
    slot = _normalize_defense_slot(pos)
    return slot if slot in {"1b", "2b", "3b", "ss"} else None


def _normalize_outfield_slot(pos: str | None) -> str | None:
    slot = _normalize_defense_slot(pos)
    return slot if slot in {"lf", "cf", "rf"} else None


def _normalize_catcher_slot(pos: str | None) -> str | None:
    slot = _normalize_defense_slot(pos)
    return slot if slot == "c" else None


def _extract_starting_infield_slots(
    players: dict[str, BoxscorePlayer],
) -> dict[str, int]:
    slots: dict[str, int] = {}
    for p in players.values():
        if p.person is None or p.person.id is None:
            continue
        # Boxscore includes bench players with their primary position. Restrict
        # to active on-field defenders to avoid duplicate slot noise.
        if p.gameStatus is not None and p.gameStatus.isOnBench:
            continue
        pos_abbr = p.position.abbreviation if p.position else None
        slot = _normalize_infield_slot(pos_abbr)
        if slot is None and p.allPositions:
            for ap in p.allPositions:
                slot = _normalize_infield_slot(ap.abbreviation if ap else None)
                if slot is not None:
                    break
        if slot is None:
            continue
        if slot in slots and slots[slot] != p.person.id:
            continue
        slots[slot] = p.person.id
    return slots


def _extract_starting_outfield_slots(
    players: dict[str, BoxscorePlayer],
) -> dict[str, int]:
    slots: dict[str, int] = {}
    for p in players.values():
        if p.person is None or p.person.id is None:
            continue
        if p.gameStatus is not None and p.gameStatus.isOnBench:
            continue
        pos_abbr = p.position.abbreviation if p.position else None
        slot = _normalize_outfield_slot(pos_abbr)
        if slot is None and p.allPositions:
            for ap in p.allPositions:
                slot = _normalize_outfield_slot(ap.abbreviation if ap else None)
                if slot is not None:
                    break
        if slot is None:
            continue
        if slot in slots and slots[slot] != p.person.id:
            continue
        slots[slot] = p.person.id
    return slots


def _extract_starting_catcher_id(
    players: dict[str, BoxscorePlayer],
) -> int | None:
    for p in players.values():
        if p.person is None or p.person.id is None:
            continue
        if p.gameStatus is not None and p.gameStatus.isOnBench:
            continue
        pos_abbr = p.position.abbreviation if p.position else None
        slot = _normalize_catcher_slot(pos_abbr)
        if slot is None and p.allPositions:
            for ap in p.allPositions:
                slot = _normalize_catcher_slot(ap.abbreviation if ap else None)
                if slot is not None:
                    break
        if slot == "c":
            return p.person.id
    return None


def _pickoff_target_base(event_type: str | None, description: str | None = None) -> str | None:
    """Return pickoff base label (1B/2B/3B) parsed from event type/description."""
    et = (event_type or "").lower()
    m = re.search(r"pickoff_([123]b)", et)
    if m:
        return m.group(1).upper()

    desc = (description or "").upper()
    m = re.search(r"\b([123]B)\b", desc)
    if m:
        return m.group(1)
    return None


def _parse_appearance(play: AllPlay, players: dict[str, GameDataPlayer]) -> _Appearance:
    """Convert a single AllPlay into an _Appearance with pre-parsed events."""
    events: list[Any] = []
    all_runners = play.runners or []
    explicit_runner_event_keys: set[
        tuple[
            int | None,
            str | None,
            str | None,
            bool,
            str,
            int | None,
            bool,
            str | None,
        ]
    ] = set()

    for pe in play.playEvents or []:
        details = pe.details
        if pe.isPitch:
            coords = pe.pitchData.coordinates if pe.pitchData else None
            type_obj = details.type if details else None
            events.append(
                _PitchEvent(
                    description=(details.description or "") if details else "",
                    pitch_type_code=(type_obj.code or "") if type_obj else "",
                    speed=pe.pitchData.startSpeed if pe.pitchData else None,
                    px=coords.pX if coords else None,
                    pz=coords.pZ if coords else None,
                    hit_x=(
                        pe.hitData.coordinates.coordX
                        if pe.hitData and pe.hitData.coordinates
                        else None
                    ),
                    hit_y=(
                        pe.hitData.coordinates.coordY
                        if pe.hitData and pe.hitData.coordinates
                        else None
                    ),
                )
            )
        elif pe.isSubstitution:
            in_id = pe.player.id if pe.player else None
            out_id = pe.replacedPlayer.id if pe.replacedPlayer else None
            if out_id is not None:
                in_p = players.get(f"ID{in_id}") if in_id else None
                out_p = players.get(f"ID{out_id}")
                events.append(
                    _SubEvent(
                        in_player_id=in_id,
                        in_last_name=(in_p.lastName or "?").upper() if in_p else "?",
                        out_last_name=(out_p.lastName or "?").upper() if out_p else "?",
                        out_player_id=out_id,
                    )
                )
            else:
                p = players.get(f"ID{in_id}") if in_id else None
                pos = (pe.position.abbreviation or "?") if pe.position else "?"
                events.append(
                    _SwitchEvent(
                        in_player_id=in_id,
                        last_name=(p.lastName or "?").upper() if p else "?",
                        new_position=pos,
                    )
                )
        elif pe.isBaseRunningPlay:
            player_id = pe.player.id if pe.player else None
            event_type_str = (details.eventType or "") if details else ""
            desc = (details.description or "") if details else ""
            if "pickoff" in event_type_str.lower():
                # Pickoffs are modeled from play.runners where base and out result
                # are explicit (pickoff_{1b,2b,3b} + movement.isOut).
                continue
            else:
                # Find runner movement in the play's runner list
                is_scoring = False
                play_index: int | None = None
                is_out = False
                start_base: str | None = None
                end_base: str | None = None
                out_base: str | None = None
                for r in all_runners:
                    if (
                        r.details
                        and r.details.runner
                        and r.details.runner.id == player_id
                    ):
                        is_scoring = bool(r.details.isScoringEvent)
                        play_index = r.details.playIndex
                        if r.movement:
                            start_base = r.movement.start
                            end_base = r.movement.end
                            is_out = bool(r.movement.isOut)
                            out_base = r.movement.outBase
                        break
                p = players.get(f"ID{player_id}") if player_id else None
                events.append(
                    _RunnerEvent(
                        player_id=player_id,
                        last_name=(p.lastName or "?").upper() if p else "?",
                        event_type=event_type_str,
                        play_index=play_index,
                        is_scoring=is_scoring,
                        is_out=is_out,
                        start_base=start_base,
                        end_base=end_base,
                        out_base=out_base,
                        run_description=desc.upper(),
                    )
                )
                explicit_runner_event_keys.add(
                    (
                        player_id,
                        start_base,
                        end_base,
                        is_scoring,
                        event_type_str.lower(),
                        play_index,
                        is_out,
                        out_base,
                    )
                )

    # Fallback: many plays report runner movement only in play.runners, without
    # dedicated isBaseRunningPlay entries in playEvents.
    for runner in all_runners:
        details = runner.details
        movement = runner.movement
        runner_ref = details.runner if details else None
        player_id = runner_ref.id if runner_ref else None
        event_type = ((details.eventType or "") if details else "").lower()
        if "pickoff" in event_type:
            pickoff_desc = getattr(details, "description", None) if details else None
            target_base = _pickoff_target_base(event_type, pickoff_desc)
            if target_base is None:
                continue
            events.append(
                _PickoffEvent(
                    description=(pickoff_desc or (details.event or "") if details else ""),
                    target_base=target_base,
                    is_out=bool(movement.isOut) if movement else False,
                )
            )
            continue
        if "strikeout" in event_type:
            continue

        is_scoring = bool(details.isScoringEvent) if details else False
        play_index = details.playIndex if details else None
        start_base = movement.start if movement else None
        end_base = movement.end if movement else None
        is_out = bool(movement.isOut) if movement else False
        out_base = movement.outBase if movement else None
        runner_key = (
            player_id,
            start_base,
            end_base,
            is_scoring,
            event_type,
            play_index,
            is_out,
            out_base,
        )
        if runner_key in explicit_runner_event_keys:
            continue
        if not is_scoring and start_base is None and end_base is None and not (is_out and out_base is not None):
            logger.warning(
                "Unaccounted runner event: player=%s event=%s is_out=%s out_base=%s play_index=%s",
                player_id, event_type, is_out, out_base, play_index,
            )
            continue

        p = players.get(f"ID{player_id}") if player_id else None
        desc = (
            details.event
            or details.movementReason
            or details.eventType
            or "ADVANCE"
        ) if details else "ADVANCE"
        events.append(
            _RunnerEvent(
                player_id=player_id,
                last_name=(p.lastName or "?").upper() if p else "?",
                event_type=details.eventType if details else None,
                play_index=play_index,
                is_scoring=is_scoring,
                is_out=is_out,
                start_base=start_base,
                end_base=end_base,
                out_base=out_base,
                run_description=desc.upper(),
            )
        )
    scoring_count = sum(
        1 for r in all_runners if r.details and r.details.isScoringEvent
    )
    batter_id = (play.matchup.batter.id or 0) if (play.matchup and play.matchup.batter) else 0
    batter_last_name = "?"
    if batter_id:
        batter_player = players.get(f"ID{batter_id}")
        if batter_player and batter_player.lastName:
            batter_last_name = batter_player.lastName.upper()
    pitcher_id = (
        (play.matchup.pitcher.id or 0)
        if (play.matchup and play.matchup.pitcher)
        else 0
    )

    return _Appearance(
        batter_id=batter_id,
        batter_last_name=batter_last_name,
        pitcher_id=pitcher_id,
        pa_summary=(play.result.event or "") if play.result else "",
        pa_event_type=(play.result.eventType or "") if play.result else "",
        is_error=(play.result.eventType == "field_error") if play.result else False,
        scoring_runner_count=scoring_count,
        inning_outs=(play.count.outs or 0) if play.count else 0,
        end_time_str=play.about.endTime if play.about else None,
        events=events,
    )


def _parse_feed(feed: GameFeed) -> _GameData:
    """Parse a GameFeed into a _GameData wrapper."""
    game_data_node = feed.gameData
    players_raw = (
        (game_data_node.players.root if game_data_node.players else None)
        if game_data_node
        else None
    ) or {}
    players: dict[str, GameDataPlayer] = dict(players_raw)

    live_data = feed.liveData
    boxscore = live_data.boxscore if live_data else None
    teams_bs = boxscore.teams if boxscore else None
    away_bs = teams_bs.away if teams_bs else None
    home_bs = teams_bs.home if teams_bs else None

    away_batting_order = (away_bs.battingOrder or []) if away_bs else []
    home_batting_order = (home_bs.battingOrder or []) if home_bs else []

    away_players_raw = (
        (away_bs.players.root or {}) if (away_bs and away_bs.players) else {}
    )
    home_players_raw = (
        (home_bs.players.root or {}) if (home_bs and home_bs.players) else {}
    )
    away_players: dict[str, BoxscorePlayer] = dict(away_players_raw)
    home_players: dict[str, BoxscorePlayer] = dict(home_players_raw)
    away_starting_lineup_slots = _extract_starting_lineup_slots(away_players)
    home_starting_lineup_slots = _extract_starting_lineup_slots(home_players)
    away_starting_lineup_slots = _fill_lineup_slots_from_order(
        away_starting_lineup_slots,
        away_batting_order,
    )
    home_starting_lineup_slots = _fill_lineup_slots_from_order(
        home_starting_lineup_slots,
        home_batting_order,
    )
    away_starting_infield_slots = _extract_starting_infield_slots(away_players)
    home_starting_infield_slots = _extract_starting_infield_slots(home_players)
    away_starting_outfield_slots = _extract_starting_outfield_slots(away_players)
    home_starting_outfield_slots = _extract_starting_outfield_slots(home_players)
    away_starting_catcher_id = _extract_starting_catcher_id(away_players)
    home_starting_catcher_id = _extract_starting_catcher_id(home_players)

    decisions = live_data.decisions if live_data else None
    winner_id = (
        (decisions.winner.id if decisions.winner else None) if decisions else None
    )
    loser_id = (decisions.loser.id if decisions.loser else None) if decisions else None

    plays = live_data.plays if live_data else None
    all_plays = (plays.allPlays or []) if plays else []
    plays_by_inning = (plays.playsByInning or []) if plays else []

    innings: list[tuple[_HalfInning, _HalfInning]] = []
    for item in plays_by_inning:
        top_apps = [
            _parse_appearance(all_plays[i], players)
            for i in (item.top or [])
            if i < len(all_plays)
        ]
        bottom_apps = [
            _parse_appearance(all_plays[i], players)
            for i in (item.bottom or [])
            if i < len(all_plays)
        ]
        innings.append((_HalfInning(top_apps), _HalfInning(bottom_apps)))

    return _GameData(
        innings=innings,
        away_batting_order=away_batting_order,
        home_batting_order=home_batting_order,
        away_starting_lineup_slots=away_starting_lineup_slots,
        home_starting_lineup_slots=home_starting_lineup_slots,
        away_starting_infield_slots=away_starting_infield_slots,
        home_starting_infield_slots=home_starting_infield_slots,
        away_starting_outfield_slots=away_starting_outfield_slots,
        home_starting_outfield_slots=home_starting_outfield_slots,
        away_starting_catcher_id=away_starting_catcher_id,
        home_starting_catcher_id=home_starting_catcher_id,
        away_players=away_players,
        home_players=home_players,
        game_data_players=players,
        winner_id=winner_id,
        loser_id=loser_id,
    )


class DisplayMode(Enum):
    MAIN_MENU = auto()
    GAME_SELECT = auto()
    REPLAY = auto()
    LIVE = auto()
    PREVIEW = auto()
    SETTINGS = auto()
    PLAYERS = auto()


_TAB_MODES: list["DisplayMode"] = [
    DisplayMode.REPLAY,
    DisplayMode.LIVE,
    DisplayMode.PREVIEW,
]


# Players screen state


class PlayersBrowseState(BaseModel):
    selected_team_index: int = 0
    selected_player_index: int = 0

    def current_team(self) -> TeamInfo | None:
        teams = get_teams()
        if not teams:
            return None
        idx = max(0, min(self.selected_team_index, len(teams) - 1))
        return teams[idx]

    def current_player(self) -> RosterEntry | None:
        team = self.current_team()
        if team is None:
            return None
        roster = get_roster(team.id)
        if not roster:
            return None
        idx = max(0, min(self.selected_player_index, len(roster) - 1))
        return roster[idx]

    def handle_scroll_x(self, increment: int) -> None:
        teams = get_teams()
        if not teams:
            return
        self.selected_team_index = (self.selected_team_index + increment) % len(teams)
        self.selected_player_index = 0

    def handle_scroll_y(self, increment: int) -> None:
        team = self.current_team()
        if team is None:
            return
        roster = get_roster(team.id)
        if not roster:
            return
        self.selected_player_index = (self.selected_player_index + increment) % len(
            roster
        )


class PlayersStatsState(BaseModel):
    player_mlb_id: int
    player_name: str
    player_number: str
    player_position: str
    player_team_abbr: str
    selected_tab_index: int = 0
    scroll_offset: int = 0
    available_years: list[str] = Field(default_factory=list)
    available_year_teams: dict[str, str] = Field(default_factory=dict)

    def tab_list(self) -> list[tuple[str, str, str | None]]:
        """Return (label, stat_type, season_or_None) for every visible tab."""
        tabs: list[tuple[str, str, str | None]] = [
            ("CAREER", "career", None),
        ]
        for yr in self.available_years:
            tabs.append((f"{yr} SEASON", "yearByYear", yr))
        return tabs

    def current_tab(self) -> tuple[str, str, str | None]:
        tabs = self.tab_list()
        idx = min(self.selected_tab_index, len(tabs) - 1)
        return tabs[idx]

    def handle_scroll_x(self, increment: int) -> None:
        self.selected_tab_index = (self.selected_tab_index + increment) % len(
            self.tab_list()
        )

    def handle_scroll_y(self, increment: int) -> None:
        self.scroll_offset += increment


class PlayersState(BaseModel):
    sub_mode: str = "browse"  # "browse" | "stats"
    browse: PlayersBrowseState = Field(default_factory=PlayersBrowseState)
    stats: PlayersStatsState | None = None

    def handle_scroll_x(self, increment: int) -> None:
        if self.sub_mode == "browse":
            self.browse.handle_scroll_x(increment)
        elif self.sub_mode == "stats" and self.stats is not None:
            self.stats.handle_scroll_x(increment)

    def handle_scroll_y(self, increment: int) -> None:
        if self.sub_mode == "browse":
            self.browse.handle_scroll_y(increment)
        elif self.sub_mode == "stats" and self.stats is not None:
            self.stats.handle_scroll_y(increment)

    def enter_stats_mode(self) -> None:
        player = self.browse.current_player()
        team = self.browse.current_team()
        if player is None or team is None:
            return
        self.stats = PlayersStatsState(
            player_mlb_id=player.mlb_id,
            player_name=player.full_name,
            player_number=player.jersey_number,
            player_position=player.position,
            player_team_abbr=team.abbreviation,
        )
        self.sub_mode = "stats"

    def exit_stats_mode(self) -> None:
        self.sub_mode = "browse"
        self.stats = None


class SettingsState(BaseModel):
    selected_row: int = 0
    editing: bool = False
    pending_option_index: int = 0

    def _current_option_index(self) -> int:
        rate = get_settings().refresh_rate
        try:
            return REFRESH_RATE_OPTIONS.index(rate)
        except ValueError:
            return 0

    def enter_edit(self) -> None:
        self.pending_option_index = self._current_option_index()
        self.editing = True

    def confirm_edit(self) -> None:
        set_refresh_rate(REFRESH_RATE_OPTIONS[self.pending_option_index])
        self.editing = False

    def cancel_edit(self) -> None:
        self.editing = False

    def handle_scroll_y(self, increment: int) -> None:
        if not self.editing:
            self.selected_row = min(
                max(self.selected_row + increment, 0), len(SETTINGS_ROWS) - 1
            )

    def handle_scroll_x(self, increment: int) -> None:
        if self.editing:
            self.pending_option_index = min(
                max(self.pending_option_index + increment, 0),
                len(REFRESH_RATE_OPTIONS) - 1,
            )


class MainMenuState(BaseModel):
    selected_row: int = 0

    def handle_scroll_y(self, increment: int) -> None:
        self.selected_row = min(
            max(self.selected_row + increment, 0), len(MAIN_MENU_ITEMS) - 1
        )

    def selected_item(self) -> str:
        return MAIN_MENU_ITEMS[self.selected_row]


def _inferred_game_end_time(game: ScheduledGame) -> datetime:
    # Schedule rows don't provide a reliable end timestamp. For tab placement,
    # treat stale "Live" games as finished once they are well past first pitch.
    return game.game_date + timedelta(hours=6)


def _effective_game_status(game: ScheduledGame, now: datetime | None = None) -> str:
    now = now or datetime.now().astimezone()
    if game.status == "Live" and _inferred_game_end_time(game) <= now:
        return "Final"
    return game.status


class GameSelectState(BaseModel):
    tab_index: int = 1
    scroll_offset: int = 0
    selected_row: int = 0
    rows: list[ScheduledGame] = []

    def reset(self) -> None:
        self.scroll_offset = 0
        self.selected_row = 0
        # Default to Live tab; fall back to Preview if no Live games exist
        self.tab_index = 1
        self.update_rows()
        if not self.rows:
            self.tab_index = 2
            self.update_rows()

    def update_rows(self) -> None:
        all_rows = sorted(get_available_games(), key=lambda g: g.game_date)
        now = datetime.now().astimezone()
        rows = [
            row
            for row in all_rows
            if _effective_game_status(row, now) == TAB_STATUSES[self.tab_index]
        ]
        # Finished tab (index 0) shows most recently started game first
        if self.tab_index == 0:
            rows = list(reversed(rows))
        self.rows = rows

    def handle_scroll_x(self, increment: int):
        _old_index = self.tab_index
        self.tab_index = min(max(self.tab_index + increment, 0), len(TABS) - 1)
        if self.tab_index == _old_index:
            return  # nothing else to do

        self.update_rows()
        self.scroll_offset = 0
        self.selected_row = 0

    def handle_scroll_y(self, increment: int):
        self.selected_row = min(
            max(self.selected_row + increment, 0), len(self.rows) - 1
        )
        if self.selected_row < self.scroll_offset:
            self.scroll_offset = self.selected_row
        elif self.selected_row >= self.scroll_offset + MENU_NUM_ROWS:
            self.scroll_offset = self.selected_row - MENU_NUM_ROWS + 1

    def get_selected_game(self) -> Optional[ScheduledGame]:
        if not self.rows:
            return None
        return self.rows[self.selected_row]


class ReplayState(BaseModel):
    clock_time: datetime = Field(default_factory=datetime.now)

    # even is top half, odd is bottom half
    inning_index: int = 0

    @property
    def current_inning(self) -> int:
        return self.inning_index // 2

    @property
    def is_top_half(self) -> bool:
        return self.inning_index % 2 == 0

    current_appearance: int = 0

    def get_appearance(self) -> _Appearance | None:
        gd = get_game_data_parsed()
        if not gd:
            return None
        inning_idx = self.inning_index // 2
        if inning_idx >= len(gd.innings):
            return None
        top, bottom = gd.innings[inning_idx]
        appearances = (
            top.appearances if self.inning_index % 2 == 0 else bottom.appearances
        )
        if self.current_appearance >= len(appearances):
            return None
        return appearances[self.current_appearance]

    def get_num_innings(self) -> int:
        gd = get_game_data_parsed()
        if not gd:
            return 0
        n = 2 * len(gd.innings)
        if gd.innings and not gd.innings[-1][1].appearances:
            n -= 1
        return n

    def get_num_appearances(self) -> int:
        gd = get_game_data_parsed()
        if not gd:
            return 0
        inning_idx = self.inning_index // 2
        if inning_idx >= len(gd.innings):
            return 0
        top, bottom = gd.innings[inning_idx]
        appearances = (
            top.appearances if self.inning_index % 2 == 0 else bottom.appearances
        )
        return len(appearances)

    def increment_inning(self, increment: int) -> None:
        current = self.inning_index
        num_innings = self.get_num_innings()
        self.inning_index = min(max(current + increment, 0), num_innings - 1)
        if self.inning_index != current:
            self.current_appearance = 0

    def increment_appearance(self, increment: int) -> None:
        num_appearances = self.get_num_appearances()
        self.current_appearance += increment
        if self.current_appearance < 0:
            if self.inning_index == 0:
                self.current_appearance = 0
            else:
                self.increment_inning(-1)
                self.current_appearance = self.get_num_appearances() - 1
        elif self.current_appearance >= num_appearances:
            if self.inning_index == self.get_num_innings() - 1:
                self.current_appearance = num_appearances - 1
            else:
                self.increment_inning(1)
                self.current_appearance = 0

        app = self.get_appearance()
        if not app:
            return
        if app.end_time_str:
            try:
                self.clock_time = datetime.fromisoformat(app.end_time_str)
            except ValueError:
                pass

    def reset_to_end(self, game_data: _GameData) -> None:
        innings = game_data.innings
        if not innings:
            self.inning_index = 0
            self.current_appearance = 0
            return
        last_idx = len(innings) - 1
        top, bottom = innings[last_idx]
        if bottom.appearances:
            self.inning_index = last_idx * 2 + 1
            self.current_appearance = len(bottom.appearances) - 1
        elif top.appearances:
            self.inning_index = last_idx * 2
            self.current_appearance = len(top.appearances) - 1
        else:
            self.inning_index = 0
            self.current_appearance = 0


class InningData(BaseModel):
    top: int | None = None
    bottom: int | None = None

    def reset(self):
        self.top = None
        self.bottom = None

    def zero(self):
        self.top = 0
        self.bottom = 0

    def add_top(self, inc: int):
        self.top = (self.top or 0) + inc

    def add_bottom(self, inc: int):
        self.bottom = (self.bottom or 0) + inc

    def add(self, is_top: bool, inc: int) -> None:
        """Add *inc* to either the top or bottom half-inning total."""
        if is_top:
            self.add_top(inc)
        else:
            self.add_bottom(inc)


class DisplayData(BaseModel):
    inning_runs: list[InningData] = []
    runs: InningData = Field(default_factory=InningData)
    hits: InningData = Field(default_factory=InningData)
    errors: InningData = Field(default_factory=InningData)

    balls: int = 0
    strikes: int = 0
    outs: int = 0

    active_inning_idx: int | None = None
    active_is_top_half: bool = True

    current_batter_mlb_id: int | None = None
    batting_is_away: bool = True
    current_pitcher_mlb_id: int | None = None

    pa_events: list[PAEvent] = Field(default_factory=list)  # type: ignore[assignment]

    # All pitch locations for the current PA: (x, y, category)
    pitch_locations: list[tuple[float, float, str]] = Field(default_factory=list)  # type: ignore[assignment]

    last_pitch_speed: float | None = None
    last_pitch_position: tuple[float, float] | None = None
    last_hit_position: tuple[float, float] | None = None
    runner_ids_by_base: dict[str, int] = Field(default_factory=dict)
    runner_last_names_by_id: dict[int, str] = Field(default_factory=_default_runner_name_map)
    runner_numbers_by_id: dict[int, str] = Field(default_factory=_default_runner_number_map)
    remaining_runner_starts_by_base: dict[str, int] = Field(default_factory=dict)
    runner_numbers_by_base: dict[str, str] = Field(default_factory=dict)
    runner_animation_pa_token: tuple[int, bool, int] | None = None
    runner_animation_max_play_index: int | None = None
    runner_animation_full_pa: bool = False
    runner_animation_moves: list[RunnerAnimationMove] = Field(
        default_factory=_default_runner_animation_moves
    )
    runner_animation_segments: list[tuple[str, str]] = Field(
        default_factory=_default_base_segment_list
    )
    show_strikeout_k: bool = False
    pickoff_target_base: str | None = None
    pickoff_succeeds: bool | None = None
    away_lineup_slots: dict[int, int] = Field(default_factory=_default_lineup_slots)
    home_lineup_slots: dict[int, int] = Field(default_factory=_default_lineup_slots)
    away_infield_slots: dict[str, int] = Field(default_factory=_default_infield_slots)
    home_infield_slots: dict[str, int] = Field(default_factory=_default_infield_slots)
    away_outfield_slots: dict[str, int] = Field(default_factory=_default_outfield_slots)
    home_outfield_slots: dict[str, int] = Field(default_factory=_default_outfield_slots)
    away_catcher_id: int | None = None
    home_catcher_id: int | None = None
    defender_numbers_by_id: dict[int, str] = Field(default_factory=_default_runner_number_map)

    clock: str = "--:--"

    lineup: list[LineupEntry] = Field(default_factory=list)  # type: ignore[assignment]
    batter_info: BatterInfo | None = None
    batter_season_stats: HittingStats | None = None
    batter_career_stats: HittingStats | None = None
    pitcher_info: PitcherInfo | None = None
    pitcher_season_stats: PitchingStats | None = None
    pitcher_career_stats: PitchingStats | None = None
    away_team_id: int | None = None
    home_team_id: int | None = None

    def set_clock(self, dt: datetime | None = None) -> None:
        dt = dt or datetime.now().astimezone()
        self.clock = _strip_hour_zero(dt.strftime("%I:%M"))

    def start_appearance(self):
        self.balls = 0
        self.strikes = 0
        self.pa_events = []
        self.pitch_locations = []
        self.last_hit_position = None
        self.runner_animation_max_play_index = None
        self.runner_animation_moves = []
        self.runner_animation_segments = []
        self.show_strikeout_k = False
        self.pickoff_target_base = None
        self.pickoff_succeeds = None

    def observe_appearance(
        self,
        appearance: _Appearance,
        inning_idx: int,
        is_top_half: bool,
        appearance_idx: int = 0,
    ):
        half_inning_changed = (
            self.active_inning_idx != inning_idx
            or self.active_is_top_half != is_top_half
        )
        if half_inning_changed:
            self.runner_ids_by_base = {}
            self.runner_last_names_by_id = _default_runner_name_map()
            self.remaining_runner_starts_by_base = {}
            self.runner_numbers_by_base = {}

        self.start_appearance()
        # Set side before processing events so substitutions mutate the proper lineup.
        self.batting_is_away = is_top_half
        # Set batter/pitcher IDs up front so per-event handlers can key off current batter.
        self.current_batter_mlb_id = appearance.batter_id
        self.current_pitcher_mlb_id = appearance.pitcher_id
        self.runner_animation_pa_token = (inning_idx, is_top_half, appearance_idx)
        self._update_runner_animation_metadata(appearance)

        if not appearance.events:
            self.active_inning_idx = inning_idx
            self.active_is_top_half = is_top_half
            return

        if appearance.batter_id:
            self.runner_ids_by_base["home"] = appearance.batter_id
            self.runner_last_names_by_id[appearance.batter_id] = appearance.batter_last_name
        start_counts: dict[str, int] = {}
        for event in appearance.events:
            if isinstance(event, _RunnerEvent):
                start_base = self._normalize_base_name(event.start_base)
                if start_base is not None:
                    start_counts[start_base] = start_counts.get(start_base, 0) + 1
        self.remaining_runner_starts_by_base = start_counts
        saw_in_play_pitch = False
        for event in appearance.events:
            if isinstance(event, _PitchEvent):
                if "in play" in event.description.lower():
                    saw_in_play_pitch = True
                self._observe_pitch_event(event)
            elif isinstance(event, _RunnerEvent):
                self._observe_runner_event(event)
            elif isinstance(event, _SubEvent):
                self._observe_substitution_event(event)
            elif isinstance(event, _SwitchEvent):
                self._observe_switch_event(event)
            elif isinstance(event, _PickoffEvent):
                self._observe_pickoff_event(event)
            else:
                logger.warning(
                    "Unknown event type in plate appearance: %s", type(event).__name__
                )

        is_strikeout = appearance.pa_summary == "Strikeout"
        if is_strikeout:
            self.runner_ids_by_base.pop("home", None)
            self.show_strikeout_k = True
            self.pa_events.append(
                PAEvent(
                    text=f"{appearance.batter_last_name} STRIKES OUT",
                    category="strike",
                )
            )
        elif (appearance.pa_event_type or "").lower() == "field_out":
            # MLB feed doesn't always include a runner movement row for batter outs,
            # so explicitly log field_out outcomes for PA event display.
            summary = (appearance.pa_summary or "OUT").upper()
            self.pa_events.append(
                PAEvent(
                    text=f"{appearance.batter_last_name} {summary}",
                    category="advance",
                )
            )
        elif saw_in_play_pitch:
            self.runner_ids_by_base.pop("home", None)

        is_hit = appearance.pa_summary in ("Single", "Double", "Triple", "Home Run")
        self.inning_runs[inning_idx].add(is_top_half, appearance.scoring_runner_count)
        self.runs.add(is_top_half, appearance.scoring_runner_count)
        self.hits.add(is_top_half, 1 if is_hit else 0)
        self.errors.add(is_top_half, 1 if appearance.is_error else 0)
        self.outs = appearance.inning_outs
        self.active_inning_idx = inning_idx
        self.active_is_top_half = is_top_half
        self.current_batter_mlb_id = appearance.batter_id
        self.current_pitcher_mlb_id = appearance.pitcher_id

    def _active_lineup_slots(self) -> dict[int, int]:
        return self.away_lineup_slots if self.batting_is_away else self.home_lineup_slots

    def _active_defense_infield_slots(self) -> dict[str, int]:
        # Defense is opposite of batting side.
        return self.home_infield_slots if self.batting_is_away else self.away_infield_slots

    def _active_defense_outfield_slots(self) -> dict[str, int]:
        # Defense is opposite of batting side.
        return self.home_outfield_slots if self.batting_is_away else self.away_outfield_slots

    def _active_defense_catcher_id(self) -> int | None:
        return self.home_catcher_id if self.batting_is_away else self.away_catcher_id

    def _set_active_defense_catcher_id(self, catcher_id: int | None) -> None:
        if self.batting_is_away:
            self.home_catcher_id = catcher_id
        else:
            self.away_catcher_id = catcher_id

    @staticmethod
    def _find_boxscore_player_by_id(
        players: dict[str, BoxscorePlayer],
        player_id: int | None,
    ) -> BoxscorePlayer | None:
        if player_id is None:
            return None
        direct = players.get(f"ID{player_id}")
        if direct is not None:
            return direct
        for p in players.values():
            if p.person is not None and p.person.id == player_id:
                return p
        return None

    @staticmethod
    def _find_game_data_player_by_id(
        players: dict[str, GameDataPlayer],
        player_id: int | None,
    ) -> GameDataPlayer | None:
        if player_id is None:
            return None
        direct = players.get(f"ID{player_id}")
        if direct is not None:
            return direct
        for p in players.values():
            if p.id == player_id:
                return p
        return None

    @staticmethod
    def _normalize_base_name(base: str | None) -> str | None:
        if base is None:
            return None
        key = base.strip().lower()
        mapping: dict[str, str] = {
            "home": "home",
            "home plate": "home",
            "1b": "1b",
            "1st": "1b",
            "first": "1b",
            "2b": "2b",
            "2nd": "2b",
            "second": "2b",
            "3b": "3b",
            "3rd": "3b",
            "third": "3b",
        }
        return mapping.get(key)

    def _remove_runner_from_bases(self, player_id: int) -> None:
        to_remove = [base for base, pid in self.runner_ids_by_base.items() if pid == player_id]
        for base in to_remove:
            self.runner_ids_by_base.pop(base, None)

    @staticmethod
    def _next_base(base: str) -> str | None:
        order: dict[str, str | None] = {
            "1b": "2b",
            "2b": "3b",
            "3b": "home",
            "home": None,
        }
        return order.get(base)

    @staticmethod
    def _next_base_for_path(base: str) -> str | None:
        order: dict[str, str | None] = {
            "home": "1b",
            "1b": "2b",
            "2b": "3b",
            "3b": "home",
        }
        return order.get(base)

    def _movement_segments(
        self, start_base: str, end_base: str | None, is_out: bool
    ) -> list[tuple[str, str]]:
        if not is_out and start_base == "home" and end_base == "home":
            # Home runs (or equivalent null->score batter moves) should animate
            # around the full basepath rather than collapsing to a point.
            return [
                ("home", "1b"),
                ("1b", "2b"),
                ("2b", "3b"),
                ("3b", "home"),
            ]
        if end_base is None:
            if is_out:
                nxt = self._next_base_for_path(start_base)
                return [(start_base, nxt)] if nxt is not None else []
            return []
        if start_base == end_base:
            return []
        segments: list[tuple[str, str]] = []
        current = start_base
        for _ in range(4):
            nxt = self._next_base_for_path(current)
            if nxt is None:
                break
            segments.append((current, nxt))
            if nxt == end_base:
                break
            current = nxt
        return segments

    def _update_runner_animation_metadata(self, appearance: _Appearance) -> None:
        moves_by_index: dict[int, list[RunnerAnimationMove]] = {}
        for event in appearance.events:
            if not isinstance(event, _RunnerEvent):
                continue
            if event.play_index is None or event.player_id is None:
                continue
            if "strikeout" in (event.event_type or "").lower():
                continue

            start_base = self._normalize_base_name(event.start_base)
            end_base = self._normalize_base_name(event.end_base)
            if start_base is None and event.player_id == appearance.batter_id:
                start_base = "home"
            if start_base is None and event.is_out and event.out_base is not None:
                start_base = "home"
            if start_base is None:
                continue

            if event.is_scoring:
                anim_end = "home"
            elif event.is_out:
                anim_end = self._normalize_base_name(event.out_base)
            else:
                anim_end = end_base
                if anim_end is None:
                    continue

            move = RunnerAnimationMove(
                player_id=event.player_id,
                last_name=event.last_name,
                start_base=start_base,
                end_base=anim_end,
                is_out=event.is_out,
                play_index=event.play_index,
            )
            moves_by_index.setdefault(event.play_index, []).append(move)

        if not moves_by_index:
            return

        max_index = max(moves_by_index)
        if self.runner_animation_full_pa:
            raw_active_moves = [
                move
                for play_index in sorted(moves_by_index)
                for move in moves_by_index[play_index]
            ]
        else:
            raw_active_moves = moves_by_index[max_index]
        # Combine chained movement events for the same runner into one animation
        # from the earliest start base to the final end state.
        combined_data: dict[int, dict[str, Any]] = {}
        combined_order: list[int] = []
        for move in raw_active_moves:
            pid = move.player_id
            if pid not in combined_data:
                combined_data[pid] = {
                    "last_name": move.last_name,
                    "start_base": move.start_base,
                    "end_base": move.end_base,
                    "is_out": move.is_out,
                    "play_index": move.play_index,
                }
                combined_order.append(pid)
                continue

            combined_data[pid]["last_name"] = move.last_name
            combined_data[pid]["end_base"] = move.end_base
            combined_data[pid]["is_out"] = move.is_out

        active_moves = [
            RunnerAnimationMove(
                player_id=pid,
                last_name=str(combined_data[pid]["last_name"]),
                start_base=str(combined_data[pid]["start_base"]),
                end_base=(
                    str(combined_data[pid]["end_base"])
                    if combined_data[pid]["end_base"] is not None
                    else None
                ),
                is_out=bool(combined_data[pid]["is_out"]),
                play_index=int(combined_data[pid]["play_index"]),
            )
            for pid in combined_order
        ]
        self.runner_animation_max_play_index = max_index
        self.runner_animation_moves = active_moves

        segments: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for move in active_moves:
            for segment in self._movement_segments(
                move.start_base, move.end_base, move.is_out
            ):
                if segment in seen:
                    continue
                seen.add(segment)
                segments.append(segment)
        self.runner_animation_segments = segments

    def _force_advance_from_base(self, base: str) -> None:
        runner_id = self.runner_ids_by_base.get(base)
        if runner_id is None:
            return
        runner_name = self.runner_last_names_by_id.get(runner_id, "RUNNER")

        next_base = self._next_base(base)
        self.runner_ids_by_base.pop(base, None)
        if next_base is None or next_base == "home":
            self.pa_events.append(
                PAEvent(text=f"{runner_name} SCORES", category="run")
            )
            return

        occupant = self.runner_ids_by_base.get(next_base)
        if occupant is not None and occupant != runner_id:
            self._force_advance_from_base(next_base)
        self.runner_ids_by_base[next_base] = runner_id
        self.pa_events.append(
            PAEvent(
                text=f"{runner_name} FORCED TO {self._format_base_label(next_base)}",
                category="advance",
            )
        )

    @staticmethod
    def _format_base_label(base: str | None) -> str:
        mapping: dict[str, str] = {
            "home": "HOME",
            "1b": "1B",
            "2b": "2B",
            "3b": "3B",
        }
        return mapping.get(base or "", "BASE")

    def _target_base_for_runner_event(
        self,
        event_type: str | None,
        start_base: str | None,
        end_base: str | None,
    ) -> str:
        et = (event_type or "").lower()
        m = re.search(r"(?:stolen_base|caught_stealing)_([123]b|home)", et)
        if m:
            parsed = self._normalize_base_name(m.group(1))
            return self._format_base_label(parsed)
        if end_base is not None:
            return self._format_base_label(end_base)
        if start_base is not None:
            return self._format_base_label(start_base)
        return "BASE"

    def _reset_pitch_display(self) -> None:
        self.last_pitch_speed = None
        self.last_pitch_position = None

    def _observe_pitch_event(self, pitch: _PitchEvent) -> None:
        desc = pitch.description
        # update pitch count
        if "Ball" in desc:
            self.balls += 1
        elif "Strike" in desc:
            self.strikes += 1
        elif "Foul" in desc and self.strikes < 2:
            self.strikes += 1
        if desc == "Foul Tip" and self.strikes == 2:
            self.strikes = 3

        ptype_str = pitch.pitch_type_code
        speed = pitch.speed
        px = pitch.px
        pz = pitch.pz
        hit_x = pitch.hit_x
        hit_y = pitch.hit_y
        position: tuple[float, float] | None = (
            (px, pz) if px is not None and pz is not None else None
        )
        hit_position: tuple[float, float] | None = (
            (hit_x, hit_y) if hit_x is not None and hit_y is not None else None
        )

        self.last_pitch_speed = speed
        self.last_pitch_position = position
        self.last_hit_position = hit_position

        full_name: str = PITCH_TYPE_NAMES.get(ptype_str, ptype_str) if ptype_str else ""
        desc_lower = desc.lower()
        if "in play" in desc_lower:
            right_text = "IN PLAY"
            category = "in_play"
        elif "ball" in desc_lower and "foul" not in desc_lower:
            right_text = "BALL"
            category = "ball"
        elif "swinging" in desc_lower:
            right_text = "SWINGING STRIKE"
            category = "strike"
        elif "called" in desc_lower:
            right_text = "CALLED STRIKE"
            category = "strike"
        elif "foul tip" in desc_lower:
            right_text = "FOUL TIP"
            category = "strike"
        elif "foul" in desc_lower:
            right_text = "FOUL"
            category = "strike"
        elif "hit by pitch" in desc_lower:
            right_text = "HIT BY PITCH"
            category = "ball"
        else:
            right_text = desc.upper()
            category = "strike"
        self.pa_events.append(
            PAEvent(text=full_name, right_text=right_text, category=category)
        )
        if position is not None:
            self.pitch_locations.append((position[0], position[1], category))

    def _observe_runner_event(self, advance: _RunnerEvent) -> None:
        player_id = advance.player_id
        last_name = advance.last_name
        event_type = (advance.event_type or "").lower()
        # Strikeout runner entries are purely record-keeping; the strikeout
        # message is generated separately — skip to avoid duplicate/wrong events.
        if "strikeout" in event_type:
            return
        start_base = self._normalize_base_name(advance.start_base)
        end_base = self._normalize_base_name(advance.end_base)
        scored = advance.is_scoring
        run_desc = advance.run_description

        if start_base is not None:
            remaining = self.remaining_runner_starts_by_base.get(start_base, 0) - 1
            if remaining > 0:
                self.remaining_runner_starts_by_base[start_base] = remaining
            else:
                self.remaining_runner_starts_by_base.pop(start_base, None)

        if player_id is not None:
            self.runner_last_names_by_id[player_id] = last_name
            self._remove_runner_from_bases(player_id)
            if not scored and end_base is not None:
                occupied_runner = self.runner_ids_by_base.get(end_base)
                if occupied_runner is not None and occupied_runner != player_id:
                    # If a later explicit runner movement starts from this base,
                    # trust that event ordering instead of inferring a force now.
                    if self.remaining_runner_starts_by_base.get(end_base, 0) == 0:
                        self._force_advance_from_base(end_base)
                self.runner_ids_by_base[end_base] = player_id

        out_target = end_base or self._normalize_base_name(advance.out_base)
        # Batter outs get descriptive PA events (e.g. POP OUT / GROUNDED OUT / STRIKES OUT).
        # Suppress only the duplicate "batter out at 1B from home" runner line.
        # Keep runner out logs when a batter first reaches base, then is retired later
        # (for example: SINGLE TO 1B followed by OUT AT 2B).
        if (
            advance.is_out
            and "strikeout" not in event_type
            and player_id is not None
            and player_id == self.current_batter_mlb_id
            and out_target == "1b"
            and (start_base is None or start_base == "home")
        ):
            return

        is_home_run = (
            player_id is not None
            and player_id == self.current_batter_mlb_id
            and ("home_run" in event_type or "home run" in run_desc.lower())
        )

        if is_home_run:
            text = f"{last_name} HOME RUN"
            category = "run"
        elif scored:
            text = f"{last_name} ADVANCES TO SCORE"
            category = "run"
        elif "caught_stealing" in event_type:
            target = self._target_base_for_runner_event(event_type, start_base, end_base)
            text = f"{last_name} CAUGHT STEALING {target}"
            category = "advance"
        elif "stolen_base" in event_type:
            target = self._target_base_for_runner_event(event_type, start_base, end_base)
            text = f"{last_name} STEALS {target}"
            category = "advance"
        elif advance.is_out:
            if out_target:
                text = f"{last_name} OUT AT {self._format_base_label(out_target)}"
            else:
                text = run_desc if run_desc else f"{last_name} OUT"
            category = "advance"
        elif end_base:
            target = self._format_base_label(end_base)
            if not start_base:
                text = f"{last_name} {run_desc} TO {target}"
            else:
                text = f"{last_name} ADVANCES TO {target}"
            category = "advance"
        else:
            text = run_desc if run_desc else "OUT"
            category = "advance"
        self.pa_events.append(PAEvent(text=text, category=category))

    def _observe_substitution_event(self, sub: _SubEvent) -> None:
        text = f"SUB: {sub.in_last_name} FOR {sub.out_last_name}"
        self.pa_events.append(PAEvent(text=text, category="sub"))
        if sub.out_player_id is not None and sub.in_player_id is not None:
            # If the outgoing player is currently on a base (pinch-runner substitution),
            # replace them in the base-occupancy map and carry over the name entry.
            for base, pid in tuple(self.runner_ids_by_base.items()):
                if pid == sub.out_player_id:
                    self.runner_ids_by_base[base] = sub.in_player_id
                    self.runner_last_names_by_id[sub.in_player_id] = sub.in_last_name
                    break

            # Substitutions can affect either team (offensive or defensive), so
            # update whichever lineup currently contains the outgoing player.
            mapped = False
            for slots in (self.away_lineup_slots, self.home_lineup_slots):
                for slot, pid in tuple(slots.items()):
                    if pid == sub.out_player_id:
                        slots[slot] = sub.in_player_id
                        mapped = True
                        break
                if mapped:
                    break
            # Defensive substitution: if outgoing player occupies any tracked
            # defensive slot, replace that slot with the incoming player.
            for defense_slots in (
                self._active_defense_infield_slots(),
                self._active_defense_outfield_slots(),
            ):
                for slot, pid in tuple(defense_slots.items()):
                    if pid == sub.out_player_id:
                        defense_slots[slot] = sub.in_player_id
                        break
            if self._active_defense_catcher_id() == sub.out_player_id:
                self._set_active_defense_catcher_id(sub.in_player_id)
        if (
            sub.out_player_id is not None
            and sub.out_player_id == self.current_pitcher_mlb_id
        ):
            self._reset_pitch_display()

    def _observe_switch_event(self, switch: _SwitchEvent) -> None:
        text = f"SWITCH: {switch.last_name} -> {switch.new_position}"
        self.pa_events.append(PAEvent(text=text, category="switch"))
        slot = _normalize_defense_slot(switch.new_position)
        if slot is None or switch.in_player_id is None:
            return
        if slot == "c":
            self._set_active_defense_catcher_id(switch.in_player_id)
            return
        if self._active_defense_catcher_id() == switch.in_player_id:
            self._set_active_defense_catcher_id(None)
        defense_slots = (
            self._active_defense_infield_slots()
            if slot in {"1b", "2b", "3b", "ss"}
            else self._active_defense_outfield_slots()
        )
        # Keep one slot per player.
        for s, pid in tuple(defense_slots.items()):
            if pid == switch.in_player_id:
                defense_slots.pop(s, None)
        defense_slots[slot] = switch.in_player_id

    def _observe_pickoff_event(self, pickoff: _PickoffEvent) -> None:
        result = "SUCCEEDS" if pickoff.is_out else "FAILS"
        self.pickoff_target_base = pickoff.target_base
        self.pickoff_succeeds = pickoff.is_out
        text = f"PICKOFF ATTEMPT AT {pickoff.target_base} {result}"
        self.pa_events.append(PAEvent(text=text, category="pickoff"))

    def reset(self):
        # Reset scalar fields from fresh defaults so new fields are picked up automatically.
        _managed = frozenset({"inning_runs", "runs", "hits", "errors", "clock"})
        for name, field_info in type(self).model_fields.items():
            if name not in _managed:
                default_val = (
                    field_info.default_factory()  # type: ignore[misc]
                    if field_info.default_factory is not None
                    else field_info.default
                )
                setattr(self, name, default_val)
        for inning in self.inning_runs:
            inning.reset()
        self.runs.zero()
        self.hits.zero()
        self.errors.zero()
        self.set_clock()

    def observe_game(self, feed: GameFeed, replay_state: Optional[ReplayState] = None):
        game_data = _parse_feed(feed)
        innings = game_data.innings

        n_innings = max(9, len(innings))
        if len(self.inning_runs) > n_innings:
            self.inning_runs = self.inning_runs[:n_innings]
        else:
            while len(self.inning_runs) < n_innings:
                self.inning_runs.append(InningData())

        self.reset()
        self.runner_animation_full_pa = replay_state is not None
        self.away_lineup_slots = dict(game_data.away_starting_lineup_slots)
        self.home_lineup_slots = dict(game_data.home_starting_lineup_slots)
        self.away_infield_slots = dict(game_data.away_starting_infield_slots)
        self.home_infield_slots = dict(game_data.home_starting_infield_slots)
        self.away_outfield_slots = dict(game_data.away_starting_outfield_slots)
        self.home_outfield_slots = dict(game_data.home_starting_outfield_slots)
        self.away_catcher_id = game_data.away_starting_catcher_id
        self.home_catcher_id = game_data.home_starting_catcher_id
        for idx, (top_half, bottom_half) in enumerate(innings):
            if replay_state and idx > replay_state.current_inning:
                break

            self._reset_pitch_display()

            if top_half.appearances:
                for a_idx, appearance in enumerate(top_half.appearances):
                    if (
                        replay_state
                        and idx == replay_state.current_inning
                        and replay_state.is_top_half
                        and a_idx > replay_state.current_appearance
                    ):
                        break
                    self.observe_appearance(appearance, idx, True, a_idx)
                    if replay_state and appearance.end_time_str:
                        try:
                            self.set_clock(
                                datetime.fromisoformat(
                                    appearance.end_time_str
                                ).astimezone()
                            )
                        except ValueError:
                            pass

            if (
                replay_state
                and idx == replay_state.current_inning
                and replay_state.is_top_half
            ):
                break

            if bottom_half.appearances:
                for a_idx, appearance in enumerate(bottom_half.appearances):
                    if (
                        replay_state
                        and idx == replay_state.current_inning
                        and a_idx > replay_state.current_appearance
                    ):
                        break
                    self.observe_appearance(appearance, idx, False, a_idx)
                    if replay_state and appearance.end_time_str:
                        try:
                            self.set_clock(
                                datetime.fromisoformat(
                                    appearance.end_time_str
                                ).astimezone()
                            )
                        except ValueError:
                            pass

        self._observe_teams(game_data)

    def _observe_teams(self, game_data: _GameData) -> None:
        """Populate lineup, batter_info, and pitcher_info from the current game state."""
        batting_players = (
            game_data.away_players if self.batting_is_away else game_data.home_players
        )
        batting_lineup_slots = self._active_lineup_slots()
        pitching_players = (
            game_data.home_players if self.batting_is_away else game_data.away_players
        )
        id_to_number: dict[int, str] = {}
        for player in batting_players.values():
            if player.person is None or player.person.id is None:
                continue
            id_to_number[player.person.id] = player.jerseyNumber or ""
        self.runner_numbers_by_id = id_to_number
        self.runner_numbers_by_base = {
            base: id_to_number[pid]
            for base, pid in self.runner_ids_by_base.items()
            if pid in id_to_number and id_to_number[pid]
        }

        defender_numbers: dict[int, str] = {}
        for player in pitching_players.values():
            if player.person is None or player.person.id is None:
                continue
            defender_numbers[player.person.id] = player.jerseyNumber or ""
        self.defender_numbers_by_id = defender_numbers

        # --- lineup ---
        lineup: list[LineupEntry] = []
        for slot in range(1, 10):
            pid = batting_lineup_slots.get(slot)
            if pid is None:
                continue
            player = self._find_boxscore_player_by_id(batting_players, pid)
            if player is not None and player.person is not None:
                mlb_id = player.person.id or pid
                full_name = player.person.fullName or "?"
                num = player.jerseyNumber or ""
            else:
                fallback_player = self._find_game_data_player_by_id(
                    game_data.game_data_players,
                    pid,
                )
                if fallback_player is None:
                    logger.warning("Missing lineup player for slot %s (id=%s)", slot, pid)
                    continue
                mlb_id = fallback_player.id or pid
                full_name = fallback_player.fullName or fallback_player.lastName or "?"
                num = fallback_player.primaryNumber or ""
            is_active = mlb_id == self.current_batter_mlb_id
            # derive last name: everything after the last space, or full name if no space
            last_name = full_name.split(" ", 1)[-1].upper()[:LINEUP_NAME_MAX_CHARS]
            lineup.append(
                LineupEntry(
                    last_name=last_name,
                    number=num,
                    mlb_id=mlb_id,
                    is_active=is_active,
                )
            )
        self.lineup = lineup

        # --- batter info ---
        current_batter: BoxscorePlayer | None = self._find_boxscore_player_by_id(
            batting_players,
            self.current_batter_mlb_id,
        )
        if current_batter is not None and current_batter.person is not None:
            full_name_b = current_batter.person.fullName or ""
            _b_display_name = full_name_b.upper()
            _b_number = current_batter.jerseyNumber or ""
            bs = current_batter.stats.batting if current_batter.stats else None
            self.batter_info = BatterInfo(
                display_name=_b_display_name,
                number=_b_number,
                ab=_fmt_stat(bs.atBats if bs else None),
                h=_fmt_stat(bs.hits if bs else None),
                r=_fmt_stat(bs.runs if bs else None),
                rbi=_fmt_stat(bs.rbi if bs else None),
                bb=_fmt_stat(bs.baseOnBalls if bs else None),
                so=_fmt_stat(bs.strikeOuts if bs else None),
            )
        else:
            gd_batter = self._find_game_data_player_by_id(
                game_data.game_data_players,
                self.current_batter_mlb_id,
            )
            if gd_batter is not None:
                name = gd_batter.fullName or gd_batter.lastName or "UNKNOWN"
                self.batter_info = BatterInfo(
                    display_name=name.upper(),
                    number=gd_batter.primaryNumber or "",
                    ab="-",
                    h="-",
                    r="-",
                    rbi="-",
                    bb="-",
                    so="-",
                )
                logger.warning(
                    "Batter id %s missing in batting boxscore players; using gameData fallback",
                    self.current_batter_mlb_id,
                )
            else:
                self.batter_info = None

        # --- batter season/career stats ---
        batter_id: int = self.current_batter_mlb_id or 0
        if batter_id:
            raw_season = get_player_stats(batter_id, "season", "hitting")
            self.batter_season_stats = (
                _build_hitting_stats(raw_season) if raw_season else None
            )
            raw_career = get_player_stats(batter_id, "career", "hitting")
            self.batter_career_stats = (
                _build_hitting_stats(raw_career) if raw_career else None
            )
        else:
            self.batter_season_stats = None
            self.batter_career_stats = None

        # --- pitcher info ---
        current_pitcher: BoxscorePlayer | None = self._find_boxscore_player_by_id(
            pitching_players,
            self.current_pitcher_mlb_id,
        )

        if current_pitcher is not None and current_pitcher.person is not None:
            full_name_p = current_pitcher.person.fullName or ""
            display_name = full_name_p.upper()
            _p_number = current_pitcher.jerseyNumber or ""
            ps = current_pitcher.stats.pitching if current_pitcher.stats else None
            ss = (
                current_pitcher.seasonStats.pitching
                if current_pitcher.seasonStats
                else None
            )
            pitcher_id = current_pitcher.person.id or 0
            if game_data.winner_id is not None and game_data.winner_id == pitcher_id:
                wls = "W"
            elif game_data.loser_id is not None and game_data.loser_id == pitcher_id:
                wls = "L"
            elif ps and (ps.saves or 0) > 0:
                wls = "S"
            else:
                wls = "-"
            self.pitcher_info = PitcherInfo(
                display_name=display_name,
                number=_p_number,
                ip=(ps.inningsPitched or "-") if ps else "-",
                h=_fmt_stat(ps.hits if ps else None),
                r=_fmt_stat(ps.runs if ps else None),
                er=_fmt_stat(ps.earnedRuns if ps else None),
                so=_fmt_stat(ps.strikeOuts if ps else None),
                bb=_fmt_stat(ps.baseOnBalls if ps else None),
                p=_fmt_stat(ps.numberOfPitches if ps else None),
                s=_fmt_stat(ps.strikes if ps else None),
                wls=wls,
                era=(ss.era or "-") if ss else "-",
                whip=(ss.whip or "-") if ss else "-",
            )
        else:
            gd_pitcher = self._find_game_data_player_by_id(
                game_data.game_data_players,
                self.current_pitcher_mlb_id,
            )
            if gd_pitcher is not None:
                pname = gd_pitcher.fullName or gd_pitcher.lastName or "UNKNOWN"
                self.pitcher_info = PitcherInfo(
                    display_name=pname.upper(),
                    number=gd_pitcher.primaryNumber or "",
                    ip="-",
                    h="-",
                    r="-",
                    er="-",
                    so="-",
                    bb="-",
                    p="-",
                    s="-",
                    wls="-",
                    era="-",
                    whip="-",
                )
            else:
                self.pitcher_info = None

        # --- pitcher season/career stats ---
        if current_pitcher is not None and current_pitcher.person is not None:
            pitcher_id_for_stats: int = current_pitcher.person.id or 0
            raw_p_season = get_player_stats(pitcher_id_for_stats, "season", "pitching")
            self.pitcher_season_stats = (
                _build_pitching_stats(raw_p_season) if raw_p_season else None
            )
            raw_p_career = get_player_stats(pitcher_id_for_stats, "career", "pitching")
            self.pitcher_career_stats = (
                _build_pitching_stats(raw_p_career) if raw_p_career else None
            )
        else:
            self.pitcher_season_stats = None
            self.pitcher_career_stats = None


class State(BaseModel):
    mode: DisplayMode

    # main menu
    main_menu: MainMenuState = Field(default_factory=MainMenuState)

    # game select variables
    game_select: GameSelectState = Field(default_factory=GameSelectState)

    # selected game
    selected_game: ScheduledGame | None = None

    # game replay
    replay: ReplayState = Field(default_factory=ReplayState)

    # settings
    settings_menu: SettingsState = Field(default_factory=SettingsState)

    # players
    players: PlayersState = Field(default_factory=PlayersState)

    def handle_scroll_x(self, increment: int):
        if self.mode == DisplayMode.GAME_SELECT:
            self.game_select.handle_scroll_x(increment)
        elif self.mode == DisplayMode.REPLAY:
            self.replay.increment_inning(increment)
        elif self.mode == DisplayMode.SETTINGS:
            self.settings_menu.handle_scroll_x(increment)
        elif self.mode == DisplayMode.PLAYERS:
            self.players.handle_scroll_x(increment)

    def handle_scroll_y(self, increment: int):
        if self.mode == DisplayMode.GAME_SELECT:
            self.game_select.handle_scroll_y(increment)
        elif self.mode == DisplayMode.MAIN_MENU:
            self.main_menu.handle_scroll_y(increment)
        elif self.mode == DisplayMode.REPLAY:
            self.replay.increment_appearance(increment)
        elif self.mode == DisplayMode.SETTINGS:
            self.settings_menu.handle_scroll_y(increment)
        elif self.mode == DisplayMode.PLAYERS:
            self.players.handle_scroll_y(increment)

    def handle_click_x(self):
        if self.mode == DisplayMode.MAIN_MENU:
            if self.main_menu.selected_item() == "Games":
                self.mode = DisplayMode.GAME_SELECT
                self.game_select.reset()
            elif self.main_menu.selected_item() == "Player Stats":
                self.mode = DisplayMode.PLAYERS
                self.players = PlayersState()  # reset browse state
            elif self.main_menu.selected_item() == "Settings":
                self.mode = DisplayMode.SETTINGS
        elif self.mode == DisplayMode.GAME_SELECT:
            selected = self.game_select.get_selected_game()
            if selected is not None:
                self.selected_game = selected
                self.mode = _TAB_MODES[self.game_select.tab_index]
        elif self.mode == DisplayMode.SETTINGS:
            if self.settings_menu.editing:
                self.settings_menu.confirm_edit()
            else:
                self.settings_menu.enter_edit()
        elif self.mode == DisplayMode.PLAYERS:
            if self.players.sub_mode == "browse":
                self.players.enter_stats_mode()

    def handle_click_y(self):
        global _game_data, _game_data_key
        if self.mode == DisplayMode.GAME_SELECT:
            self.mode = DisplayMode.MAIN_MENU
        elif self.mode == DisplayMode.SETTINGS:
            if self.settings_menu.editing:
                self.settings_menu.cancel_edit()
            else:
                self.mode = DisplayMode.MAIN_MENU
        elif self.mode == DisplayMode.PLAYERS:
            if self.players.sub_mode == "stats":
                self.players.exit_stats_mode()
            else:
                self.mode = DisplayMode.MAIN_MENU
        elif self.mode not in (DisplayMode.MAIN_MENU, DisplayMode.GAME_SELECT):
            self.mode = DisplayMode.GAME_SELECT
            self.game_select.reset()
            self.selected_game = None
            _game_data = None
            _game_data_key = None
            _game_display_data.reset()


_state = State(mode=DisplayMode.MAIN_MENU)
_game_data_key: Optional[str] = None
_game_data: Optional[GameFeed] = None
_game_data_parsed: Optional[_GameData] = None
_game_display_data: DisplayData = DisplayData()
_last_update_time: float = 0.0


def get_state() -> State:
    return _state


def get_game_data() -> Optional[GameFeed]:
    return _game_data


def get_game_data_parsed() -> Optional[_GameData]:
    return _game_data_parsed


def get_game_display_data() -> DisplayData:
    return _game_display_data


def initialize_startup_mode(team_abbr: str = "NYM") -> None:
    """Set initial mode/game based on live or upcoming games for *team_abbr*."""
    team_key = team_abbr.upper()
    now = datetime.now().astimezone()
    games = sorted(get_available_games(), key=lambda g: g.game_date)

    def is_team_game(game: ScheduledGame) -> bool:
        return game.away_team.upper() == team_key or game.home_team.upper() == team_key

    live_game = next(
        (g for g in games if _effective_game_status(g, now) == "Live" and is_team_game(g)),
        None,
    )
    if live_game is not None:
        _state.selected_game = live_game
        _state.mode = DisplayMode.LIVE
        return

    upcoming_game = next(
        (
            g
            for g in games
            if _effective_game_status(g, now) == "Preview"
            and is_team_game(g)
            and g.game_date >= now
        ),
        None,
    )
    if upcoming_game is not None:
        _state.selected_game = upcoming_game
        _state.mode = DisplayMode.PREVIEW
        return

    _state.selected_game = None
    _state.mode = DisplayMode.MAIN_MENU


def update_state() -> None:
    global _game_data_key, _game_data, _game_data_parsed, _game_display_data, _last_update_time
    selected = get_state().selected_game

    if not selected:
        return

    # PREVIEW: switch to LIVE if countdown expired (checked every frame, cheap)
    if _state.mode == DisplayMode.PREVIEW:
        if selected.game_date <= datetime.now().astimezone():
            _state.mode = DisplayMode.LIVE

    now = time.monotonic()
    if now - _last_update_time >= get_settings().refresh_rate:
        _last_update_time = now

        selected_key = selected.key
        is_new_game = selected_key != _game_data_key

        # PREVIEW: also refresh schedule to detect Live status from the API
        if _state.mode == DisplayMode.PREVIEW:
            fresh = next(
                (g for g in get_available_games() if g.key == selected_key), None
            )
            if fresh and _effective_game_status(fresh, datetime.now().astimezone()) == "Live":
                _state.selected_game = fresh
                _state.mode = DisplayMode.LIVE

        if is_new_game or _state.mode == DisplayMode.LIVE:
            feed = get_live_game(selected.game_pk)
            if feed is not None:
                _game_data = feed
                _game_data_parsed = _parse_feed(feed)
            else:
                _game_data = None
                _game_data_parsed = None
            _game_data_key = selected_key
            if is_new_game and _game_data_parsed and _state.mode == DisplayMode.REPLAY:
                _state.replay.reset_to_end(_game_data_parsed)

    if _game_data:
        _game_display_data.observe_game(
            _game_data, _state.replay if _state.mode == DisplayMode.REPLAY else None
        )
        _game_display_data.away_team_id = selected.away_team_id
        _game_display_data.home_team_id = selected.home_team_id
    else:
        _game_display_data.reset()


def handle_event(event: Event) -> None:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            get_state().handle_scroll_x(1)
        elif event.key == pygame.K_LEFT:
            get_state().handle_scroll_x(-1)
        elif event.key == pygame.K_DOWN:
            get_state().handle_scroll_y(1)
        elif event.key == pygame.K_UP:
            get_state().handle_scroll_y(-1)
        elif event.key == pygame.K_RETURN:
            get_state().handle_click_x()
        elif event.key == pygame.K_SPACE:
            get_state().handle_click_y()
