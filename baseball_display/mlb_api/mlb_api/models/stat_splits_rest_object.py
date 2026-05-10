from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conference_rest_object import ConferenceRestObject
    from ..models.division_rest_object import DivisionRestObject
    from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
    from ..models.league_rest_object import LeagueRestObject
    from ..models.person_rest_object import PersonRestObject
    from ..models.schedule_item_rest_object import ScheduleItemRestObject
    from ..models.sport_rest_object import SportRestObject
    from ..models.team_rest_object import TeamRestObject
    from ..models.venue_rest_object import VenueRestObject


T = TypeVar("T", bound="StatSplitsRestObject")


@_attrs_define
class StatSplitsRestObject:
    """
    Attributes:
        away_team (TeamRestObject | Unset):
        date (datetime.date | Unset): Date of Game. Format: MM/DD/YYYY
        day_of_week (int | Unset):
        game_type (str | Unset): Type of Game. Available types in /api/v1/gameTypes
        group (str | Unset):
        home_team (TeamRestObject | Unset):
        is_home (bool | Unset):
        is_win (bool | Unset):
        league (LeagueRestObject | Unset):
        month (int | Unset):
        num_occurrences (int | Unset):
        num_teams (int | Unset):
        opponent (TeamRestObject | Unset):
        opponent_conference (ConferenceRestObject | Unset):
        opponent_division (DivisionRestObject | Unset):
        player (PersonRestObject | Unset):
        rank (int | Unset):
        schedule_item_rest_object (ScheduleItemRestObject | Unset):
        season (str | Unset): Season of play
        split (DynamicEnumRestObject | Unset):
        sport (SportRestObject | Unset):
        stat (Any | Unset):
        team (TeamRestObject | Unset):
        type_ (str | Unset):
        venue (VenueRestObject | Unset):
    """

    away_team: TeamRestObject | Unset = UNSET
    date: datetime.date | Unset = UNSET
    day_of_week: int | Unset = UNSET
    game_type: str | Unset = UNSET
    group: str | Unset = UNSET
    home_team: TeamRestObject | Unset = UNSET
    is_home: bool | Unset = UNSET
    is_win: bool | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    month: int | Unset = UNSET
    num_occurrences: int | Unset = UNSET
    num_teams: int | Unset = UNSET
    opponent: TeamRestObject | Unset = UNSET
    opponent_conference: ConferenceRestObject | Unset = UNSET
    opponent_division: DivisionRestObject | Unset = UNSET
    player: PersonRestObject | Unset = UNSET
    rank: int | Unset = UNSET
    schedule_item_rest_object: ScheduleItemRestObject | Unset = UNSET
    season: str | Unset = UNSET
    split: DynamicEnumRestObject | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    stat: Any | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    type_: str | Unset = UNSET
    venue: VenueRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.person_rest_object import PersonRestObject
        from ..models.schedule_item_rest_object import ScheduleItemRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.venue_rest_object import VenueRestObject

        away_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.away_team, Unset):
            away_team = self.away_team.to_dict()

        date: str | Unset = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        day_of_week = self.day_of_week

        game_type = self.game_type

        group = self.group

        home_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.home_team, Unset):
            home_team = self.home_team.to_dict()

        is_home = self.is_home

        is_win = self.is_win

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        month = self.month

        num_occurrences = self.num_occurrences

        num_teams = self.num_teams

        opponent: dict[str, Any] | Unset = UNSET
        if not isinstance(self.opponent, Unset):
            opponent = self.opponent.to_dict()

        opponent_conference: dict[str, Any] | Unset = UNSET
        if not isinstance(self.opponent_conference, Unset):
            opponent_conference = self.opponent_conference.to_dict()

        opponent_division: dict[str, Any] | Unset = UNSET
        if not isinstance(self.opponent_division, Unset):
            opponent_division = self.opponent_division.to_dict()

        player: dict[str, Any] | Unset = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        rank = self.rank

        schedule_item_rest_object: dict[str, Any] | Unset = UNSET
        if not isinstance(self.schedule_item_rest_object, Unset):
            schedule_item_rest_object = self.schedule_item_rest_object.to_dict()

        season = self.season

        split: dict[str, Any] | Unset = UNSET
        if not isinstance(self.split, Unset):
            split = self.split.to_dict()

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        stat = self.stat

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        type_ = self.type_

        venue: dict[str, Any] | Unset = UNSET
        if not isinstance(self.venue, Unset):
            venue = self.venue.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if away_team is not UNSET:
            field_dict["awayTeam"] = away_team
        if date is not UNSET:
            field_dict["date"] = date
        if day_of_week is not UNSET:
            field_dict["dayOfWeek"] = day_of_week
        if game_type is not UNSET:
            field_dict["gameType"] = game_type
        if group is not UNSET:
            field_dict["group"] = group
        if home_team is not UNSET:
            field_dict["homeTeam"] = home_team
        if is_home is not UNSET:
            field_dict["isHome"] = is_home
        if is_win is not UNSET:
            field_dict["isWin"] = is_win
        if league is not UNSET:
            field_dict["league"] = league
        if month is not UNSET:
            field_dict["month"] = month
        if num_occurrences is not UNSET:
            field_dict["numOccurrences"] = num_occurrences
        if num_teams is not UNSET:
            field_dict["numTeams"] = num_teams
        if opponent is not UNSET:
            field_dict["opponent"] = opponent
        if opponent_conference is not UNSET:
            field_dict["opponentConference"] = opponent_conference
        if opponent_division is not UNSET:
            field_dict["opponentDivision"] = opponent_division
        if player is not UNSET:
            field_dict["player"] = player
        if rank is not UNSET:
            field_dict["rank"] = rank
        if schedule_item_rest_object is not UNSET:
            field_dict["scheduleItemRestObject"] = schedule_item_rest_object
        if season is not UNSET:
            field_dict["season"] = season
        if split is not UNSET:
            field_dict["split"] = split
        if sport is not UNSET:
            field_dict["sport"] = sport
        if stat is not UNSET:
            field_dict["stat"] = stat
        if team is not UNSET:
            field_dict["team"] = team
        if type_ is not UNSET:
            field_dict["type"] = type_
        if venue is not UNSET:
            field_dict["venue"] = venue

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.person_rest_object import PersonRestObject
        from ..models.schedule_item_rest_object import ScheduleItemRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.venue_rest_object import VenueRestObject

        d = dict(src_dict)
        _away_team = d.pop("awayTeam", UNSET)
        away_team: TeamRestObject | Unset
        if isinstance(_away_team, Unset):
            away_team = UNSET
        else:
            away_team = TeamRestObject.from_dict(_away_team)

        _date = d.pop("date", UNSET)
        date: datetime.date | Unset
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        day_of_week = d.pop("dayOfWeek", UNSET)

        game_type = d.pop("gameType", UNSET)

        group = d.pop("group", UNSET)

        _home_team = d.pop("homeTeam", UNSET)
        home_team: TeamRestObject | Unset
        if isinstance(_home_team, Unset):
            home_team = UNSET
        else:
            home_team = TeamRestObject.from_dict(_home_team)

        is_home = d.pop("isHome", UNSET)

        is_win = d.pop("isWin", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        month = d.pop("month", UNSET)

        num_occurrences = d.pop("numOccurrences", UNSET)

        num_teams = d.pop("numTeams", UNSET)

        _opponent = d.pop("opponent", UNSET)
        opponent: TeamRestObject | Unset
        if isinstance(_opponent, Unset):
            opponent = UNSET
        else:
            opponent = TeamRestObject.from_dict(_opponent)

        _opponent_conference = d.pop("opponentConference", UNSET)
        opponent_conference: ConferenceRestObject | Unset
        if isinstance(_opponent_conference, Unset):
            opponent_conference = UNSET
        else:
            opponent_conference = ConferenceRestObject.from_dict(_opponent_conference)

        _opponent_division = d.pop("opponentDivision", UNSET)
        opponent_division: DivisionRestObject | Unset
        if isinstance(_opponent_division, Unset):
            opponent_division = UNSET
        else:
            opponent_division = DivisionRestObject.from_dict(_opponent_division)

        _player = d.pop("player", UNSET)
        player: PersonRestObject | Unset
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = PersonRestObject.from_dict(_player)

        rank = d.pop("rank", UNSET)

        _schedule_item_rest_object = d.pop("scheduleItemRestObject", UNSET)
        schedule_item_rest_object: ScheduleItemRestObject | Unset
        if isinstance(_schedule_item_rest_object, Unset):
            schedule_item_rest_object = UNSET
        else:
            schedule_item_rest_object = ScheduleItemRestObject.from_dict(
                _schedule_item_rest_object
            )

        season = d.pop("season", UNSET)

        _split = d.pop("split", UNSET)
        split: DynamicEnumRestObject | Unset
        if isinstance(_split, Unset):
            split = UNSET
        else:
            split = DynamicEnumRestObject.from_dict(_split)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        stat = d.pop("stat", UNSET)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        type_ = d.pop("type", UNSET)

        _venue = d.pop("venue", UNSET)
        venue: VenueRestObject | Unset
        if isinstance(_venue, Unset):
            venue = UNSET
        else:
            venue = VenueRestObject.from_dict(_venue)

        stat_splits_rest_object = cls(
            away_team=away_team,
            date=date,
            day_of_week=day_of_week,
            game_type=game_type,
            group=group,
            home_team=home_team,
            is_home=is_home,
            is_win=is_win,
            league=league,
            month=month,
            num_occurrences=num_occurrences,
            num_teams=num_teams,
            opponent=opponent,
            opponent_conference=opponent_conference,
            opponent_division=opponent_division,
            player=player,
            rank=rank,
            schedule_item_rest_object=schedule_item_rest_object,
            season=season,
            split=split,
            sport=sport,
            stat=stat,
            team=team,
            type_=type_,
            venue=venue,
        )

        stat_splits_rest_object.additional_properties = d
        return stat_splits_rest_object

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
