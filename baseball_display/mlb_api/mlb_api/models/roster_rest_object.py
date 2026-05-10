from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.roster_entry_rest_object import RosterEntryRestObject


T = TypeVar("T", bound="RosterRestObject")


@_attrs_define
class RosterRestObject:
    """
    Attributes:
        link (str | Unset): Link to full resource
        roster (list[RosterEntryRestObject] | Unset): All of the details of a roster
        roster_type (str | Unset): Type of roster. Available types in /api/v1/rosterTypes
        team_id (int | Unset): Unique Team Identifier. Format: 141, 147, etc
    """

    link: str | Unset = UNSET
    roster: list[RosterEntryRestObject] | Unset = UNSET
    roster_type: str | Unset = UNSET
    team_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.roster_entry_rest_object import RosterEntryRestObject

        link = self.link

        roster: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.roster, Unset):
            roster = []
            for roster_item_data in self.roster:
                roster_item = roster_item_data.to_dict()
                roster.append(roster_item)

        roster_type = self.roster_type

        team_id = self.team_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if link is not UNSET:
            field_dict["link"] = link
        if roster is not UNSET:
            field_dict["roster"] = roster
        if roster_type is not UNSET:
            field_dict["rosterType"] = roster_type
        if team_id is not UNSET:
            field_dict["teamId"] = team_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.roster_entry_rest_object import RosterEntryRestObject

        d = dict(src_dict)
        link = d.pop("link", UNSET)

        _roster = d.pop("roster", UNSET)
        roster: list[RosterEntryRestObject] | Unset = UNSET
        if _roster is not UNSET:
            roster = []
            for roster_item_data in _roster:
                roster_item = RosterEntryRestObject.from_dict(roster_item_data)

                roster.append(roster_item)

        roster_type = d.pop("rosterType", UNSET)

        team_id = d.pop("teamId", UNSET)

        roster_rest_object = cls(
            link=link,
            roster=roster,
            roster_type=roster_type,
            team_id=team_id,
        )

        roster_rest_object.additional_properties = d
        return roster_rest_object

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
