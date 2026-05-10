from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.leaders_rest_object import LeadersRestObject


T = TypeVar("T", bound="LeagueLeaderContainerRestObject")


@_attrs_define
class LeagueLeaderContainerRestObject:
    """
    Attributes:
        league_leaders (list[LeadersRestObject] | Unset):
    """

    league_leaders: list[LeadersRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.leaders_rest_object import LeadersRestObject

        league_leaders: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.league_leaders, Unset):
            league_leaders = []
            for league_leaders_item_data in self.league_leaders:
                league_leaders_item = league_leaders_item_data.to_dict()
                league_leaders.append(league_leaders_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if league_leaders is not UNSET:
            field_dict["leagueLeaders"] = league_leaders

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.leaders_rest_object import LeadersRestObject

        d = dict(src_dict)
        _league_leaders = d.pop("leagueLeaders", UNSET)
        league_leaders: list[LeadersRestObject] | Unset = UNSET
        if _league_leaders is not UNSET:
            league_leaders = []
            for league_leaders_item_data in _league_leaders:
                league_leaders_item = LeadersRestObject.from_dict(
                    league_leaders_item_data
                )

                league_leaders.append(league_leaders_item)

        league_leader_container_rest_object = cls(
            league_leaders=league_leaders,
        )

        league_leader_container_rest_object.additional_properties = d
        return league_leader_container_rest_object

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
