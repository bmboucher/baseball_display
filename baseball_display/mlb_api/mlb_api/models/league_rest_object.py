from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.season_rest_object import SeasonRestObject
    from ..models.time_zone_rest_object import TimeZoneRestObject


T = TypeVar("T", bound="LeagueRestObject")


@_attrs_define
class LeagueRestObject:
    """
    Attributes:
        abbreviation (str | Unset): Shortened version of short name. Format: ALE, SFG
        conferences_in_use (bool | Unset): Whether or not the League has Conferences
        divisions_in_use (bool | Unset): Whether or not the League has Divisions
        has_playoff_points (bool | Unset): True if a league uses points for standings
        has_split_season (bool | Unset): Whether or not there is a split season
        has_wild_card (bool | Unset): Whether or not there is a wildcard
        id (int | Unset): Unique Identifier
        link (str | Unset): Link to full resource
        name (str | Unset): Unique Name
        name_short (str | Unset): Shortened version of name. Format: AL East, SF Giants
        num_games (int | Unset): The number of regular season games
        num_teams (int | Unset): The number of teams
        num_wildcard_teams (int | Unset): The number of wildcard teams
        org_code (str | Unset): Deprecated Field
        season (str | Unset): Season of play
        season_date_info (SeasonRestObject | Unset):
        season_state (str | Unset): The status of the season. Format: offseason
        time_zone (TimeZoneRestObject | Unset):
    """

    abbreviation: str | Unset = UNSET
    conferences_in_use: bool | Unset = UNSET
    divisions_in_use: bool | Unset = UNSET
    has_playoff_points: bool | Unset = UNSET
    has_split_season: bool | Unset = UNSET
    has_wild_card: bool | Unset = UNSET
    id: int | Unset = UNSET
    link: str | Unset = UNSET
    name: str | Unset = UNSET
    name_short: str | Unset = UNSET
    num_games: int | Unset = UNSET
    num_teams: int | Unset = UNSET
    num_wildcard_teams: int | Unset = UNSET
    org_code: str | Unset = UNSET
    season: str | Unset = UNSET
    season_date_info: SeasonRestObject | Unset = UNSET
    season_state: str | Unset = UNSET
    time_zone: TimeZoneRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.season_rest_object import SeasonRestObject
        from ..models.time_zone_rest_object import TimeZoneRestObject

        abbreviation = self.abbreviation

        conferences_in_use = self.conferences_in_use

        divisions_in_use = self.divisions_in_use

        has_playoff_points = self.has_playoff_points

        has_split_season = self.has_split_season

        has_wild_card = self.has_wild_card

        id = self.id

        link = self.link

        name = self.name

        name_short = self.name_short

        num_games = self.num_games

        num_teams = self.num_teams

        num_wildcard_teams = self.num_wildcard_teams

        org_code = self.org_code

        season = self.season

        season_date_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.season_date_info, Unset):
            season_date_info = self.season_date_info.to_dict()

        season_state = self.season_state

        time_zone: dict[str, Any] | Unset = UNSET
        if not isinstance(self.time_zone, Unset):
            time_zone = self.time_zone.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if conferences_in_use is not UNSET:
            field_dict["conferencesInUse"] = conferences_in_use
        if divisions_in_use is not UNSET:
            field_dict["divisionsInUse"] = divisions_in_use
        if has_playoff_points is not UNSET:
            field_dict["hasPlayoffPoints"] = has_playoff_points
        if has_split_season is not UNSET:
            field_dict["hasSplitSeason"] = has_split_season
        if has_wild_card is not UNSET:
            field_dict["hasWildCard"] = has_wild_card
        if id is not UNSET:
            field_dict["id"] = id
        if link is not UNSET:
            field_dict["link"] = link
        if name is not UNSET:
            field_dict["name"] = name
        if name_short is not UNSET:
            field_dict["nameShort"] = name_short
        if num_games is not UNSET:
            field_dict["numGames"] = num_games
        if num_teams is not UNSET:
            field_dict["numTeams"] = num_teams
        if num_wildcard_teams is not UNSET:
            field_dict["numWildcardTeams"] = num_wildcard_teams
        if org_code is not UNSET:
            field_dict["orgCode"] = org_code
        if season is not UNSET:
            field_dict["season"] = season
        if season_date_info is not UNSET:
            field_dict["seasonDateInfo"] = season_date_info
        if season_state is not UNSET:
            field_dict["seasonState"] = season_state
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.season_rest_object import SeasonRestObject
        from ..models.time_zone_rest_object import TimeZoneRestObject

        d = dict(src_dict)
        abbreviation = d.pop("abbreviation", UNSET)

        conferences_in_use = d.pop("conferencesInUse", UNSET)

        divisions_in_use = d.pop("divisionsInUse", UNSET)

        has_playoff_points = d.pop("hasPlayoffPoints", UNSET)

        has_split_season = d.pop("hasSplitSeason", UNSET)

        has_wild_card = d.pop("hasWildCard", UNSET)

        id = d.pop("id", UNSET)

        link = d.pop("link", UNSET)

        name = d.pop("name", UNSET)

        name_short = d.pop("nameShort", UNSET)

        num_games = d.pop("numGames", UNSET)

        num_teams = d.pop("numTeams", UNSET)

        num_wildcard_teams = d.pop("numWildcardTeams", UNSET)

        org_code = d.pop("orgCode", UNSET)

        season = d.pop("season", UNSET)

        _season_date_info = d.pop("seasonDateInfo", UNSET)
        season_date_info: SeasonRestObject | Unset
        if isinstance(_season_date_info, Unset):
            season_date_info = UNSET
        else:
            season_date_info = SeasonRestObject.from_dict(_season_date_info)

        season_state = d.pop("seasonState", UNSET)

        _time_zone = d.pop("timeZone", UNSET)
        time_zone: TimeZoneRestObject | Unset
        if isinstance(_time_zone, Unset):
            time_zone = UNSET
        else:
            time_zone = TimeZoneRestObject.from_dict(_time_zone)

        league_rest_object = cls(
            abbreviation=abbreviation,
            conferences_in_use=conferences_in_use,
            divisions_in_use=divisions_in_use,
            has_playoff_points=has_playoff_points,
            has_split_season=has_split_season,
            has_wild_card=has_wild_card,
            id=id,
            link=link,
            name=name,
            name_short=name_short,
            num_games=num_games,
            num_teams=num_teams,
            num_wildcard_teams=num_wildcard_teams,
            org_code=org_code,
            season=season,
            season_date_info=season_date_info,
            season_state=season_state,
            time_zone=time_zone,
        )

        league_rest_object.additional_properties = d
        return league_rest_object

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
