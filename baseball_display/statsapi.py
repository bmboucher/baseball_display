"""MLB Stats API caching + rate-limiting wrapper.

All MLB HTTP traffic from the rest of the codebase should eventually go through
this module.  It fetches, caches, and parses MLB API responses into typed
Pydantic v2 models defined in ``baseball_display.statsapi_models``.

Rate limiting
-------------
A simple token-bucket (1 token per MIN_INTERVAL seconds) prevents accidental
IP lockouts.  The lock is per-process; the delay is only applied when a real
HTTP request is needed (cache hits are free).

Disk cache
----------
Responses are cached under ``{CACHE_DIR}/mlb_api/{hex16}.json``.
TTLs are per-endpoint-class:
    * live_game   → settings refresh-rate seconds while Live/Preview;
                                    indefinitely valid once schedule marks game Final
  * schedule    → 60 s
  * static data → 86 400 s / 24 h  (teams, roster, person, stats)

Public API
----------
  get_live_game(game_pk)            -> GameFeed | None
  get_schedule(date, sport_id=1)    -> ScheduleResponse | None  (date = "YYYY-MM-DD")
  get_teams_response(sport_id=1)        -> TeamsResponse | None
  get_roster_response(team_id, type)    -> RosterResponse | None
  get_teams()                           -> list[TeamInfo]
  get_roster(team_id)                   -> list[RosterEntry]
  get_person(person_id)             -> PersonResponse | None
  get_stats(person_id, stats, group, **extra) -> StatsResponse | None

All functions return ``None`` on any network/HTTP error or parse failure.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta, timezone
from pathlib import Path
from typing import Any, Generator, Iterable

from pydantic import BaseModel

from baseball_display.cache import make_endpoint
from baseball_display.constants import SCHEDULE_LOOKAHEAD_DAYS, SCHEDULE_LOOKBACK_DAYS
from baseball_display.mlb_api.models import (
    GameFeed,
    PersonResponse,
    RosterResponse,
    ScheduleResponse,
    StatsResponse,
    TeamsResponse,
)
from baseball_display.settings import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_BASE_URL = "https://statsapi.mlb.com"
_USER_AGENT = "baseball-display/1.0"
_REQUEST_TIMEOUT = int(os.environ.get("MLB_API_TIMEOUT", "10"))

# Minimum seconds between outbound HTTP requests for the main thread
_MIN_INTERVAL = float(os.environ.get("MLB_API_MIN_INTERVAL", "0.25"))
# Minimum seconds between requests on the background prefetch thread
_MIN_INTERVAL_PREFETCH = float(os.environ.get("MLB_API_MIN_INTERVAL_PREFETCH", "2.0"))

# TTLs in seconds
_TTL_SCHEDULE: int = 60
_TTL_STATIC: int = 86_400  # 24 h

# ---------------------------------------------------------------------------
# Rate limiter — per-thread token bucket
# ---------------------------------------------------------------------------
# Each thread has its own last-request timestamp and minimum interval so the
# slow background prefetch thread cannot starve foreground requests.

_thread_local = threading.local()


def _set_thread_min_interval(interval: float) -> None:
    """Override the minimum request interval for the calling thread."""
    _thread_local.min_interval = interval
    _thread_local.last_request_time = 0.0


def _throttle() -> None:
    if not hasattr(_thread_local, "last_request_time"):
        _thread_local.last_request_time = 0.0
    if not hasattr(_thread_local, "min_interval"):
        _thread_local.min_interval = _MIN_INTERVAL
    now = time.monotonic()
    wait = _thread_local.min_interval - (now - _thread_local.last_request_time)
    if wait > 0:
        time.sleep(wait)
    _thread_local.last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# Cache directories
# ---------------------------------------------------------------------------

_CACHE_BASE = Path(os.environ.get("CACHE_DIR", "./cache")) / "mlb_api"


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------


def _fetch(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """GET ``_BASE_URL + path`` with optional query params.  Returns parsed JSON.

    Raises ``urllib.error.URLError`` / ``ValueError`` on failure — callers wrap.
    """
    url = _BASE_URL + path
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url = url + "?" + urllib.parse.urlencode(filtered)

    logger.info(f"GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    _throttle()
    with urllib.request.urlopen(req, timeout=_REQUEST_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

# -- live_game ---------------------------------------------------------------


def _get_live_game(game_pk: int | str) -> GameFeed:
    return GameFeed.model_validate(_fetch(f"/api/v1.1/game/{game_pk}/feed/live"))


def _is_final_game(game_pk: int | str) -> bool:
    try:
        game_pk_int = int(game_pk)
    except (TypeError, ValueError):
        return False

    for g in get_available_games():
        if g.game_pk == game_pk_int:
            return g.status == "Final"
    return False


def _validate_live_game(game_pk: int | str, cache_time: float) -> bool:
    age = time.time() - cache_time
    if age <= get_settings().refresh_rate:
        return True
    # Once a game is final, cached live feed is immutable for our usage.
    return _is_final_game(game_pk)


_live_game_endpoint = make_endpoint(
    "live_game",
    _CACHE_BASE / "live_game",
    GameFeed,
    _get_live_game,
    _validate_live_game,
)


def get_live_game(game_pk: int | str) -> GameFeed | None:
    """Return the full live game feed for *game_pk*.

    Cache validity uses the configured refresh rate for live games.
    If schedule marks the game as ``Final``, cached live feed remains valid.
    Returns ``None`` on failure.
    """
    try:
        return _live_game_endpoint.get((game_pk,))
    except Exception:
        logger.exception("get_live_game failed for game_pk=%s", game_pk)
        return None


# -- schedule ----------------------------------------------------------------


def _get_schedule(date: str, sport_id: int) -> ScheduleResponse:
    return ScheduleResponse.model_validate(
        _fetch(
            "/api/v1/schedule",
            {
                "date": date,
                "sportId": sport_id,
                "hydrate": "team,linescore,flags,review",
            },
        )
    )


def _validate_schedule(date: str, sport_id: int, cache_time: float) -> bool:
    if date < datetime.date.today().isoformat():
        return True  # past dates are immutable
    return time.time() - cache_time < _TTL_SCHEDULE


_schedule_endpoint = make_endpoint(
    "schedule",
    _CACHE_BASE / "schedule",
    ScheduleResponse,
    _get_schedule,
    _validate_schedule,
)


def get_schedule(date: str, sport_id: int = 1) -> ScheduleResponse | None:
    """Return schedule for a single date (``"YYYY-MM-DD"``).

    Hydrates team, linescore, flags, and review data.
    Past dates are cached indefinitely (they never change).  Today's schedule
    is cached for ``_TTL_SCHEDULE`` seconds so live game states update promptly.
    Returns ``None`` on failure.
    """
    try:
        return _schedule_endpoint.get((date, sport_id))
    except Exception:
        logger.exception("get_schedule failed for date=%s sport_id=%s", date, sport_id)
        return None


# -- teams -------------------------------------------------------------------


def _get_teams(sport_id: int) -> TeamsResponse:
    return TeamsResponse.model_validate(_fetch("/api/v1/teams", {"sportId": sport_id}))


def _validate_teams(sport_id: int, cache_time: float) -> bool:
    return time.time() - cache_time < _TTL_STATIC


_teams_endpoint = make_endpoint(
    "teams", _CACHE_BASE / "teams", TeamsResponse, _get_teams, _validate_teams
)


def get_teams_response(sport_id: int = 1) -> TeamsResponse | None:
    """Return all MLB teams.  Cached for 24 h.  Returns ``None`` on failure."""
    try:
        return _teams_endpoint.get((sport_id,))
    except Exception:
        logger.exception("get_teams failed for sport_id=%s", sport_id)
        return None


# -- roster ------------------------------------------------------------------


def _get_roster(team_id: int, roster_type: str) -> RosterResponse:
    return RosterResponse.model_validate(
        _fetch(
            f"/api/v1/teams/{team_id}/roster/{roster_type}",
            {"hydrate": "person(fullName,primaryNumber,primaryPosition)"},
        )
    )


def _validate_roster(team_id: int, roster_type: str, cache_time: float) -> bool:
    return time.time() - cache_time < _TTL_STATIC


_roster_endpoint = make_endpoint(
    "roster", _CACHE_BASE / "roster", RosterResponse, _get_roster, _validate_roster
)


def get_roster_response(
    team_id: int, roster_type: str = "active"
) -> RosterResponse | None:
    """Return the roster for *team_id*.  Cached for 24 h.  Returns ``None`` on failure."""
    try:
        return _roster_endpoint.get((team_id, roster_type))
    except Exception:
        logger.exception(
            "get_roster failed for team_id=%s roster_type=%s", team_id, roster_type
        )
        return None


# -- person ------------------------------------------------------------------


def _get_person(person_id: int) -> PersonResponse:
    return PersonResponse.model_validate(
        _fetch(f"/api/v1/people/{person_id}", {"hydrate": "currentTeam"})
    )


def _validate_person(person_id: int, cache_time: float) -> bool:
    return time.time() - cache_time < _TTL_STATIC


_person_endpoint = make_endpoint(
    "person", _CACHE_BASE / "person", PersonResponse, _get_person, _validate_person
)


def get_person(person_id: int) -> PersonResponse | None:
    """Return biographical data for *person_id*.  Cached for 24 h.  Returns ``None`` on failure."""
    try:
        return _person_endpoint.get((person_id,))
    except Exception:
        logger.exception("get_person failed for person_id=%s", person_id)
        return None


# -- stats -------------------------------------------------------------------


def _get_stats(
    person_id: int, stats_type: str, group: str, extra_key: tuple[tuple[str, Any], ...]
) -> StatsResponse:
    params: dict[str, Any] = {"stats": stats_type, "group": group, **dict(extra_key)}
    return StatsResponse.model_validate(
        _fetch(f"/api/v1/people/{person_id}/stats", params)
    )


def _validate_stats(
    person_id: int,
    stats_type: str,
    group: str,
    extra_key: tuple[tuple[str, Any], ...],
    cache_time: float,
) -> bool:
    return time.time() - cache_time < _TTL_STATIC


_stats_endpoint = make_endpoint(
    "stats", _CACHE_BASE / "stats", StatsResponse, _get_stats, _validate_stats
)


def get_stats(
    person_id: int,
    stats: str,
    group: str,
    **extra_params: Any,
) -> StatsResponse | None:
    """Return stats for *person_id*.

    Args:
        person_id: MLB person ID.
        stats: Stat type, e.g. ``"career"``, ``"season"``, ``"yearByYear"``.
        group: Stat group, e.g. ``"hitting"``, ``"pitching"``.
        **extra_params: Additional query params (e.g. ``season="2024"``).

    Cached for 24 h.
    """
    extra_key = tuple(sorted(extra_params.items()))
    try:
        return _stats_endpoint.get((person_id, stats, group, extra_key))
    except Exception:
        logger.exception(
            "get_stats failed for person_id=%s stats=%s group=%s",
            person_id,
            stats,
            group,
        )
        return None


# ---------------------------------------------------------------------------
# TeamInfo / RosterEntry models + higher-level wrappers (from teams.py)
# ---------------------------------------------------------------------------


class TeamInfo(BaseModel, frozen=True):
    id: int
    name: str
    abbreviation: str


class RosterEntry(BaseModel, frozen=True):
    mlb_id: int
    full_name: str
    jersey_number: str
    position: str  # e.g. "RF", "SP", "C"


def get_teams() -> list[TeamInfo]:
    """Return all active MLB teams sorted by name.  Returns ``[]`` on failure."""
    response = get_teams_response()
    if response is None or not response.teams:
        return []
    teams: list[TeamInfo] = []
    for team in response.teams:
        if not team.active:
            continue
        if not (team.sport and team.sport.name == "Major League Baseball"):
            continue
        if team.id is None or team.name is None or team.abbreviation is None:
            continue
        teams.append(
            TeamInfo(id=team.id, name=team.name, abbreviation=team.abbreviation)
        )
    teams.sort(key=lambda t: t.name)
    return teams


def get_roster(team_id: int) -> list[RosterEntry]:
    """Return the active roster for *team_id* sorted by full name.  Returns ``[]`` on failure."""
    response = get_roster_response(team_id)
    if response is None or not response.roster:
        return []
    roster: list[RosterEntry] = []
    for item in response.roster:
        try:
            assert item.person is not None
            assert item.person.id is not None
            assert item.person.fullName is not None
            assert item.position is not None
            assert item.position.abbreviation is not None
            roster.append(
                RosterEntry(
                    mlb_id=item.person.id,
                    full_name=item.person.fullName,
                    jersey_number=item.jerseyNumber or "",
                    position=item.position.abbreviation,
                )
            )
        except Exception:
            logger.debug("Skipping malformed roster entry", exc_info=True)
    roster.sort(key=lambda r: r.full_name)
    return roster


# ---------------------------------------------------------------------------
# ScheduledGame model + schedule helpers (from schedule.py)
# ---------------------------------------------------------------------------


class ScheduledGame(BaseModel):
    game_date: datetime.datetime
    official_date: date
    away_team: str
    away_team_id: int
    away_team_name: str
    home_team: str
    home_team_id: int
    home_team_name: str
    game_number: int
    status: str
    venue: str | None = None
    away_score: int | None = None
    home_score: int | None = None
    game_pk: int = 0

    def to_tuple(self) -> tuple[str, str, str, int]:
        return (
            self.official_date.isoformat(),
            self.away_team,
            self.home_team,
            self.game_number,
        )

    def to_url_args(self) -> tuple[str, str, str, int]:
        return self.to_tuple()

    @property
    def key(self) -> str:
        return "-".join(map(str, self.to_tuple()))


_initialized: bool = False
_games: dict[str, ScheduledGame] = {}


def get_available_games() -> Iterable[ScheduledGame]:
    _ensure_schedule()
    return _games.values()


def _iter_games(start: date, end: date) -> Generator[ScheduledGame, None, None]:
    """Yield ScheduledGame for every game in [start, end] via the schedule endpoint."""
    d = start
    while d <= end:
        response = get_schedule(d.isoformat())
        if response:
            for date_entry in response.dates or []:
                for game in date_entry.games or []:
                    try:
                        assert game.teams is not None
                        assert game.gameDate is not None
                        assert game.officialDate is not None
                        assert game.status is not None
                        assert game.status.abstractGameState is not None
                        away = game.teams.away
                        home = game.teams.home
                        assert away is not None and away.team is not None
                        assert home is not None and home.team is not None
                        assert (
                            away.team.abbreviation is not None
                            and away.team.id is not None
                        )
                        assert (
                            home.team.abbreviation is not None
                            and home.team.id is not None
                        )
                        game_dt = datetime.datetime.fromisoformat(
                            game.gameDate.replace("Z", "+00:00")
                        ).astimezone(timezone.utc)
                        yield ScheduledGame(
                            game_date=game_dt,
                            official_date=date.fromisoformat(game.officialDate),
                            away_team=away.team.abbreviation,
                            away_team_id=away.team.id,
                            away_team_name=away.team.name or away.team.abbreviation,
                            home_team=home.team.abbreviation,
                            home_team_id=home.team.id,
                            home_team_name=home.team.name or home.team.abbreviation,
                            game_number=game.gameNumber or 1,
                            status=game.status.abstractGameState,
                            venue=game.venue.name if game.venue else None,
                            away_score=away.score,
                            home_score=home.score,
                            game_pk=game.gamePk or 0,
                        )
                    except Exception:
                        logger.debug("Skipping malformed game entry", exc_info=True)
        d += timedelta(days=1)


def _ensure_schedule() -> None:
    global _initialized

    min_date = date.today() - timedelta(days=SCHEDULE_LOOKBACK_DAYS)
    max_date = date.today() + timedelta(days=SCHEDULE_LOOKAHEAD_DAYS)

    # clean out games that are outside the range
    to_remove: list[str] = []
    for key, game in _games.items():
        if game.official_date < min_date or game.official_date > max_date:
            to_remove.append(key)
    for key in to_remove:
        del _games[key]

    # update games
    fetch_start = min_date if not _initialized else date.today()
    for game in _iter_games(fetch_start, max_date):
        _games[game.key] = game
    _initialized = True


# ---------------------------------------------------------------------------
# Player stats helpers (from player_stats.py)
# ---------------------------------------------------------------------------


def get_player_stats(
    player_id: int, stat_type: str, group: str
) -> dict[str, Any] | None:
    """Return the stat dict for (player_id, stat_type, group).

    stat_type: "season" | "career" | "yearByYear"
    group:     "hitting" | "pitching" | "fielding"

    Returns None on any failure (network error, empty response, parse error).
    """
    try:
        response = get_stats(player_id, stat_type, group)
        if response is None or not response.stats:
            return {}
        splits = response.stats[0].splits
        if not splits:
            return {}
        stat = splits[0].stat
        if stat is None:
            return {}
        return stat.model_dump(exclude_none=False)
    except Exception:
        logger.exception(
            "Failed to get player stats for player_id=%d type=%s group=%s",
            player_id,
            stat_type,
            group,
        )
        return None


def get_player_stats_by_year(
    player_id: int, group: str
) -> dict[str, dict[str, Any]] | None:
    """Return a {season: {"stat": ..., "team_id": ...}} mapping for all available seasons.

    Returns None on network/parse failure; returns {} when the API returns no data.
    """
    try:
        response = get_stats(player_id, "yearByYear", group)
        if response is None or not response.stats:
            return {}
        splits = response.stats[0].splits
        if not splits:
            return {}
        year_map: dict[str, dict[str, Any]] = {}
        for split in splits:
            if not split.season:
                continue
            stat_dict = split.stat.model_dump(exclude_none=False) if split.stat else {}
            team_id = split.team.id if split.team else None
            year_map[split.season] = {"stat": stat_dict, "team_id": team_id}
        return year_map
    except Exception:
        logger.exception(
            "Failed to get yearByYear stats for player_id=%d group=%s",
            player_id,
            group,
        )
        return None


# ---------------------------------------------------------------------------
# Background stats prefetch
# ---------------------------------------------------------------------------

_PREFETCH_STAT_TYPES = ("season", "career", "yearByYear")
_PREFETCH_GROUPS = ("hitting", "pitching")


def _prefetch_all_player_stats() -> None:
    """Pre-warm the stats cache for every player on every active roster.

    Intended to run on a daemon thread started at app launch.  All exceptions
    are swallowed so failures never affect the foreground.  Uses a slower
    per-thread rate limit so it does not starve foreground requests.
    """
    _set_thread_min_interval(_MIN_INTERVAL_PREFETCH)
    logger.info("Stats prefetch: starting")
    try:
        # 1. Pre-load the schedule window first
        min_date = date.today() - timedelta(days=SCHEDULE_LOOKBACK_DAYS)
        max_date = date.today() + timedelta(days=SCHEDULE_LOOKAHEAD_DAYS)
        d = min_date
        while d <= max_date:
            try:
                get_schedule(d.isoformat())
            except Exception:
                logger.debug("Stats prefetch: failed schedule for %s", d, exc_info=True)
            d += timedelta(days=1)
        logger.info("Stats prefetch: schedule window loaded")

        # 2. Teams, rosters, and player stats
        teams = get_teams()
        logger.info("Stats prefetch: %d teams", len(teams))
        for team in teams:
            try:
                roster = get_roster(team.id)
            except Exception:
                logger.debug(
                    "Stats prefetch: failed to get roster for %s",
                    team.abbreviation,
                    exc_info=True,
                )
                continue
            for entry in roster:
                for stat_type in _PREFETCH_STAT_TYPES:
                    for group in _PREFETCH_GROUPS:
                        try:
                            get_stats(entry.mlb_id, stat_type, group)
                        except Exception:
                            logger.debug(
                                "Stats prefetch: failed player_id=%d %s/%s",
                                entry.mlb_id,
                                stat_type,
                                group,
                                exc_info=True,
                            )
    except Exception:
        logger.exception("Stats prefetch: unexpected error")
    logger.info("Stats prefetch: complete")


def start_prefetch_thread() -> threading.Thread:
    """Start a daemon thread that pre-warms the stats cache and return it."""
    t = threading.Thread(
        target=_prefetch_all_player_stats,
        name="stats-prefetch",
        daemon=True,
    )
    t.start()
    return t
