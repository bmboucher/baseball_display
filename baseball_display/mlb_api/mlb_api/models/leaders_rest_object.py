from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.league_rest_object import LeagueRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="LeadersRestObject")


@_attrs_define
class LeadersRestObject:
    """
    Attributes:
        leader_category (str | Unset):
        league (LeagueRestObject | Unset):
        season (str | Unset):
        stat_group (str | Unset):
        team (TeamRestObject | Unset):
    """

    leader_category: str | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    season: str | Unset = UNSET
    stat_group: str | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.league_rest_object import LeagueRestObject
        from ..models.team_rest_object import TeamRestObject

        leader_category = self.leader_category

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        season = self.season

        stat_group = self.stat_group

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if leader_category is not UNSET:
            field_dict["leaderCategory"] = leader_category
        if league is not UNSET:
            field_dict["league"] = league
        if season is not UNSET:
            field_dict["season"] = season
        if stat_group is not UNSET:
            field_dict["statGroup"] = stat_group
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.league_rest_object import LeagueRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        leader_category = d.pop("leaderCategory", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        season = d.pop("season", UNSET)

        stat_group = d.pop("statGroup", UNSET)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        leaders_rest_object = cls(
            leader_category=leader_category,
            league=league,
            season=season,
            stat_group=stat_group,
            team=team,
        )

        leaders_rest_object.additional_properties = d
        return leaders_rest_object

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
