from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.league_rest_object import LeagueRestObject
    from ..models.sport_rest_object import SportRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="GamePaceRestObject")


@_attrs_define
class GamePaceRestObject:
    """
    Attributes:
        hits_per_9_inn (float | Unset):
        hits_per_game (float | Unset):
        hits_per_run (float | Unset):
        innings_played_per_game (float | Unset):
        league (LeagueRestObject | Unset):
        pitchers_per_game (float | Unset):
        pitches_per_9_inn (float | Unset):
        pitches_per_game (float | Unset):
        pitches_per_pitcher (float | Unset):
        plate_appearances_per_9_inn (float | Unset):
        plate_appearances_per_game (float | Unset):
        runs_per_9_inn (float | Unset):
        runs_per_game (float | Unset):
        season (str | Unset):
        sport (SportRestObject | Unset):
        team (TeamRestObject | Unset):
        time_per_77_plate_appearances (Any | Unset):
        time_per_7_inn_game (Any | Unset):
        time_per_7_inn_game_without_extra_inn (Any | Unset):
        time_per_9_inn (Any | Unset):
        time_per_game (Any | Unset):
        time_per_hit (Any | Unset):
        time_per_pitch (Any | Unset):
        time_per_plate_appearance (Any | Unset):
        time_per_run (Any | Unset):
        total_7_inn_games (int | Unset):
        total_7_inn_games_completed_early (int | Unset):
        total_7_inn_games_scheduled (int | Unset):
        total_7_inn_games_without_extra_inn (int | Unset):
        total_9_inn_games (int | Unset):
        total_9_inn_games_completed_early (int | Unset):
        total_9_inn_games_scheduled (int | Unset):
        total_9_inn_games_without_extra_inn (int | Unset):
        total_extra_inn_games (int | Unset):
        total_extra_inn_time (Any | Unset):
        total_game_time (Any | Unset):
        total_games (int | Unset):
        total_hits (int | Unset):
        total_innings_played (float | Unset):
        total_pitchers (int | Unset):
        total_pitches (int | Unset):
        total_plate_appearances (int | Unset):
        total_runs (int | Unset):
    """

    hits_per_9_inn: float | Unset = UNSET
    hits_per_game: float | Unset = UNSET
    hits_per_run: float | Unset = UNSET
    innings_played_per_game: float | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    pitchers_per_game: float | Unset = UNSET
    pitches_per_9_inn: float | Unset = UNSET
    pitches_per_game: float | Unset = UNSET
    pitches_per_pitcher: float | Unset = UNSET
    plate_appearances_per_9_inn: float | Unset = UNSET
    plate_appearances_per_game: float | Unset = UNSET
    runs_per_9_inn: float | Unset = UNSET
    runs_per_game: float | Unset = UNSET
    season: str | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    time_per_77_plate_appearances: Any | Unset = UNSET
    time_per_7_inn_game: Any | Unset = UNSET
    time_per_7_inn_game_without_extra_inn: Any | Unset = UNSET
    time_per_9_inn: Any | Unset = UNSET
    time_per_game: Any | Unset = UNSET
    time_per_hit: Any | Unset = UNSET
    time_per_pitch: Any | Unset = UNSET
    time_per_plate_appearance: Any | Unset = UNSET
    time_per_run: Any | Unset = UNSET
    total_7_inn_games: int | Unset = UNSET
    total_7_inn_games_completed_early: int | Unset = UNSET
    total_7_inn_games_scheduled: int | Unset = UNSET
    total_7_inn_games_without_extra_inn: int | Unset = UNSET
    total_9_inn_games: int | Unset = UNSET
    total_9_inn_games_completed_early: int | Unset = UNSET
    total_9_inn_games_scheduled: int | Unset = UNSET
    total_9_inn_games_without_extra_inn: int | Unset = UNSET
    total_extra_inn_games: int | Unset = UNSET
    total_extra_inn_time: Any | Unset = UNSET
    total_game_time: Any | Unset = UNSET
    total_games: int | Unset = UNSET
    total_hits: int | Unset = UNSET
    total_innings_played: float | Unset = UNSET
    total_pitchers: int | Unset = UNSET
    total_pitches: int | Unset = UNSET
    total_plate_appearances: int | Unset = UNSET
    total_runs: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject

        hits_per_9_inn = self.hits_per_9_inn

        hits_per_game = self.hits_per_game

        hits_per_run = self.hits_per_run

        innings_played_per_game = self.innings_played_per_game

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        pitchers_per_game = self.pitchers_per_game

        pitches_per_9_inn = self.pitches_per_9_inn

        pitches_per_game = self.pitches_per_game

        pitches_per_pitcher = self.pitches_per_pitcher

        plate_appearances_per_9_inn = self.plate_appearances_per_9_inn

        plate_appearances_per_game = self.plate_appearances_per_game

        runs_per_9_inn = self.runs_per_9_inn

        runs_per_game = self.runs_per_game

        season = self.season

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        time_per_77_plate_appearances = self.time_per_77_plate_appearances

        time_per_7_inn_game = self.time_per_7_inn_game

        time_per_7_inn_game_without_extra_inn = (
            self.time_per_7_inn_game_without_extra_inn
        )

        time_per_9_inn = self.time_per_9_inn

        time_per_game = self.time_per_game

        time_per_hit = self.time_per_hit

        time_per_pitch = self.time_per_pitch

        time_per_plate_appearance = self.time_per_plate_appearance

        time_per_run = self.time_per_run

        total_7_inn_games = self.total_7_inn_games

        total_7_inn_games_completed_early = self.total_7_inn_games_completed_early

        total_7_inn_games_scheduled = self.total_7_inn_games_scheduled

        total_7_inn_games_without_extra_inn = self.total_7_inn_games_without_extra_inn

        total_9_inn_games = self.total_9_inn_games

        total_9_inn_games_completed_early = self.total_9_inn_games_completed_early

        total_9_inn_games_scheduled = self.total_9_inn_games_scheduled

        total_9_inn_games_without_extra_inn = self.total_9_inn_games_without_extra_inn

        total_extra_inn_games = self.total_extra_inn_games

        total_extra_inn_time = self.total_extra_inn_time

        total_game_time = self.total_game_time

        total_games = self.total_games

        total_hits = self.total_hits

        total_innings_played = self.total_innings_played

        total_pitchers = self.total_pitchers

        total_pitches = self.total_pitches

        total_plate_appearances = self.total_plate_appearances

        total_runs = self.total_runs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hits_per_9_inn is not UNSET:
            field_dict["hitsPer9Inn"] = hits_per_9_inn
        if hits_per_game is not UNSET:
            field_dict["hitsPerGame"] = hits_per_game
        if hits_per_run is not UNSET:
            field_dict["hitsPerRun"] = hits_per_run
        if innings_played_per_game is not UNSET:
            field_dict["inningsPlayedPerGame"] = innings_played_per_game
        if league is not UNSET:
            field_dict["league"] = league
        if pitchers_per_game is not UNSET:
            field_dict["pitchersPerGame"] = pitchers_per_game
        if pitches_per_9_inn is not UNSET:
            field_dict["pitchesPer9Inn"] = pitches_per_9_inn
        if pitches_per_game is not UNSET:
            field_dict["pitchesPerGame"] = pitches_per_game
        if pitches_per_pitcher is not UNSET:
            field_dict["pitchesPerPitcher"] = pitches_per_pitcher
        if plate_appearances_per_9_inn is not UNSET:
            field_dict["plateAppearancesPer9Inn"] = plate_appearances_per_9_inn
        if plate_appearances_per_game is not UNSET:
            field_dict["plateAppearancesPerGame"] = plate_appearances_per_game
        if runs_per_9_inn is not UNSET:
            field_dict["runsPer9Inn"] = runs_per_9_inn
        if runs_per_game is not UNSET:
            field_dict["runsPerGame"] = runs_per_game
        if season is not UNSET:
            field_dict["season"] = season
        if sport is not UNSET:
            field_dict["sport"] = sport
        if team is not UNSET:
            field_dict["team"] = team
        if time_per_77_plate_appearances is not UNSET:
            field_dict["timePer77PlateAppearances"] = time_per_77_plate_appearances
        if time_per_7_inn_game is not UNSET:
            field_dict["timePer7InnGame"] = time_per_7_inn_game
        if time_per_7_inn_game_without_extra_inn is not UNSET:
            field_dict["timePer7InnGameWithoutExtraInn"] = (
                time_per_7_inn_game_without_extra_inn
            )
        if time_per_9_inn is not UNSET:
            field_dict["timePer9Inn"] = time_per_9_inn
        if time_per_game is not UNSET:
            field_dict["timePerGame"] = time_per_game
        if time_per_hit is not UNSET:
            field_dict["timePerHit"] = time_per_hit
        if time_per_pitch is not UNSET:
            field_dict["timePerPitch"] = time_per_pitch
        if time_per_plate_appearance is not UNSET:
            field_dict["timePerPlateAppearance"] = time_per_plate_appearance
        if time_per_run is not UNSET:
            field_dict["timePerRun"] = time_per_run
        if total_7_inn_games is not UNSET:
            field_dict["total7InnGames"] = total_7_inn_games
        if total_7_inn_games_completed_early is not UNSET:
            field_dict["total7InnGamesCompletedEarly"] = (
                total_7_inn_games_completed_early
            )
        if total_7_inn_games_scheduled is not UNSET:
            field_dict["total7InnGamesScheduled"] = total_7_inn_games_scheduled
        if total_7_inn_games_without_extra_inn is not UNSET:
            field_dict["total7InnGamesWithoutExtraInn"] = (
                total_7_inn_games_without_extra_inn
            )
        if total_9_inn_games is not UNSET:
            field_dict["total9InnGames"] = total_9_inn_games
        if total_9_inn_games_completed_early is not UNSET:
            field_dict["total9InnGamesCompletedEarly"] = (
                total_9_inn_games_completed_early
            )
        if total_9_inn_games_scheduled is not UNSET:
            field_dict["total9InnGamesScheduled"] = total_9_inn_games_scheduled
        if total_9_inn_games_without_extra_inn is not UNSET:
            field_dict["total9InnGamesWithoutExtraInn"] = (
                total_9_inn_games_without_extra_inn
            )
        if total_extra_inn_games is not UNSET:
            field_dict["totalExtraInnGames"] = total_extra_inn_games
        if total_extra_inn_time is not UNSET:
            field_dict["totalExtraInnTime"] = total_extra_inn_time
        if total_game_time is not UNSET:
            field_dict["totalGameTime"] = total_game_time
        if total_games is not UNSET:
            field_dict["totalGames"] = total_games
        if total_hits is not UNSET:
            field_dict["totalHits"] = total_hits
        if total_innings_played is not UNSET:
            field_dict["totalInningsPlayed"] = total_innings_played
        if total_pitchers is not UNSET:
            field_dict["totalPitchers"] = total_pitchers
        if total_pitches is not UNSET:
            field_dict["totalPitches"] = total_pitches
        if total_plate_appearances is not UNSET:
            field_dict["totalPlateAppearances"] = total_plate_appearances
        if total_runs is not UNSET:
            field_dict["totalRuns"] = total_runs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        hits_per_9_inn = d.pop("hitsPer9Inn", UNSET)

        hits_per_game = d.pop("hitsPerGame", UNSET)

        hits_per_run = d.pop("hitsPerRun", UNSET)

        innings_played_per_game = d.pop("inningsPlayedPerGame", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        pitchers_per_game = d.pop("pitchersPerGame", UNSET)

        pitches_per_9_inn = d.pop("pitchesPer9Inn", UNSET)

        pitches_per_game = d.pop("pitchesPerGame", UNSET)

        pitches_per_pitcher = d.pop("pitchesPerPitcher", UNSET)

        plate_appearances_per_9_inn = d.pop("plateAppearancesPer9Inn", UNSET)

        plate_appearances_per_game = d.pop("plateAppearancesPerGame", UNSET)

        runs_per_9_inn = d.pop("runsPer9Inn", UNSET)

        runs_per_game = d.pop("runsPerGame", UNSET)

        season = d.pop("season", UNSET)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        time_per_77_plate_appearances = d.pop("timePer77PlateAppearances", UNSET)

        time_per_7_inn_game = d.pop("timePer7InnGame", UNSET)

        time_per_7_inn_game_without_extra_inn = d.pop(
            "timePer7InnGameWithoutExtraInn", UNSET
        )

        time_per_9_inn = d.pop("timePer9Inn", UNSET)

        time_per_game = d.pop("timePerGame", UNSET)

        time_per_hit = d.pop("timePerHit", UNSET)

        time_per_pitch = d.pop("timePerPitch", UNSET)

        time_per_plate_appearance = d.pop("timePerPlateAppearance", UNSET)

        time_per_run = d.pop("timePerRun", UNSET)

        total_7_inn_games = d.pop("total7InnGames", UNSET)

        total_7_inn_games_completed_early = d.pop("total7InnGamesCompletedEarly", UNSET)

        total_7_inn_games_scheduled = d.pop("total7InnGamesScheduled", UNSET)

        total_7_inn_games_without_extra_inn = d.pop(
            "total7InnGamesWithoutExtraInn", UNSET
        )

        total_9_inn_games = d.pop("total9InnGames", UNSET)

        total_9_inn_games_completed_early = d.pop("total9InnGamesCompletedEarly", UNSET)

        total_9_inn_games_scheduled = d.pop("total9InnGamesScheduled", UNSET)

        total_9_inn_games_without_extra_inn = d.pop(
            "total9InnGamesWithoutExtraInn", UNSET
        )

        total_extra_inn_games = d.pop("totalExtraInnGames", UNSET)

        total_extra_inn_time = d.pop("totalExtraInnTime", UNSET)

        total_game_time = d.pop("totalGameTime", UNSET)

        total_games = d.pop("totalGames", UNSET)

        total_hits = d.pop("totalHits", UNSET)

        total_innings_played = d.pop("totalInningsPlayed", UNSET)

        total_pitchers = d.pop("totalPitchers", UNSET)

        total_pitches = d.pop("totalPitches", UNSET)

        total_plate_appearances = d.pop("totalPlateAppearances", UNSET)

        total_runs = d.pop("totalRuns", UNSET)

        game_pace_rest_object = cls(
            hits_per_9_inn=hits_per_9_inn,
            hits_per_game=hits_per_game,
            hits_per_run=hits_per_run,
            innings_played_per_game=innings_played_per_game,
            league=league,
            pitchers_per_game=pitchers_per_game,
            pitches_per_9_inn=pitches_per_9_inn,
            pitches_per_game=pitches_per_game,
            pitches_per_pitcher=pitches_per_pitcher,
            plate_appearances_per_9_inn=plate_appearances_per_9_inn,
            plate_appearances_per_game=plate_appearances_per_game,
            runs_per_9_inn=runs_per_9_inn,
            runs_per_game=runs_per_game,
            season=season,
            sport=sport,
            team=team,
            time_per_77_plate_appearances=time_per_77_plate_appearances,
            time_per_7_inn_game=time_per_7_inn_game,
            time_per_7_inn_game_without_extra_inn=time_per_7_inn_game_without_extra_inn,
            time_per_9_inn=time_per_9_inn,
            time_per_game=time_per_game,
            time_per_hit=time_per_hit,
            time_per_pitch=time_per_pitch,
            time_per_plate_appearance=time_per_plate_appearance,
            time_per_run=time_per_run,
            total_7_inn_games=total_7_inn_games,
            total_7_inn_games_completed_early=total_7_inn_games_completed_early,
            total_7_inn_games_scheduled=total_7_inn_games_scheduled,
            total_7_inn_games_without_extra_inn=total_7_inn_games_without_extra_inn,
            total_9_inn_games=total_9_inn_games,
            total_9_inn_games_completed_early=total_9_inn_games_completed_early,
            total_9_inn_games_scheduled=total_9_inn_games_scheduled,
            total_9_inn_games_without_extra_inn=total_9_inn_games_without_extra_inn,
            total_extra_inn_games=total_extra_inn_games,
            total_extra_inn_time=total_extra_inn_time,
            total_game_time=total_game_time,
            total_games=total_games,
            total_hits=total_hits,
            total_innings_played=total_innings_played,
            total_pitchers=total_pitchers,
            total_pitches=total_pitches,
            total_plate_appearances=total_plate_appearances,
            total_runs=total_runs,
        )

        game_pace_rest_object.additional_properties = d
        return game_pace_rest_object

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
