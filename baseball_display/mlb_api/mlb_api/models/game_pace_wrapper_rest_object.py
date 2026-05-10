from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.game_pace_rest_object import GamePaceRestObject


T = TypeVar("T", bound="GamePaceWrapperRestObject")


@_attrs_define
class GamePaceWrapperRestObject:
    """
    Attributes:
        leagues (list[GamePaceRestObject] | Unset):
        sports (list[GamePaceRestObject] | Unset):
        teams (list[GamePaceRestObject] | Unset):
    """

    leagues: list[GamePaceRestObject] | Unset = UNSET
    sports: list[GamePaceRestObject] | Unset = UNSET
    teams: list[GamePaceRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.game_pace_rest_object import GamePaceRestObject

        leagues: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.leagues, Unset):
            leagues = []
            for leagues_item_data in self.leagues:
                leagues_item = leagues_item_data.to_dict()
                leagues.append(leagues_item)

        sports: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sports, Unset):
            sports = []
            for sports_item_data in self.sports:
                sports_item = sports_item_data.to_dict()
                sports.append(sports_item)

        teams: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.teams, Unset):
            teams = []
            for teams_item_data in self.teams:
                teams_item = teams_item_data.to_dict()
                teams.append(teams_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if leagues is not UNSET:
            field_dict["leagues"] = leagues
        if sports is not UNSET:
            field_dict["sports"] = sports
        if teams is not UNSET:
            field_dict["teams"] = teams

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.game_pace_rest_object import GamePaceRestObject

        d = dict(src_dict)
        _leagues = d.pop("leagues", UNSET)
        leagues: list[GamePaceRestObject] | Unset = UNSET
        if _leagues is not UNSET:
            leagues = []
            for leagues_item_data in _leagues:
                leagues_item = GamePaceRestObject.from_dict(leagues_item_data)

                leagues.append(leagues_item)

        _sports = d.pop("sports", UNSET)
        sports: list[GamePaceRestObject] | Unset = UNSET
        if _sports is not UNSET:
            sports = []
            for sports_item_data in _sports:
                sports_item = GamePaceRestObject.from_dict(sports_item_data)

                sports.append(sports_item)

        _teams = d.pop("teams", UNSET)
        teams: list[GamePaceRestObject] | Unset = UNSET
        if _teams is not UNSET:
            teams = []
            for teams_item_data in _teams:
                teams_item = GamePaceRestObject.from_dict(teams_item_data)

                teams.append(teams_item)

        game_pace_wrapper_rest_object = cls(
            leagues=leagues,
            sports=sports,
            teams=teams,
        )

        game_pace_wrapper_rest_object.additional_properties = d
        return game_pace_wrapper_rest_object

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
