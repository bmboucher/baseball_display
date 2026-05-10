from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject
    from ..models.position_rest_object import PositionRestObject


T = TypeVar("T", bound="RosterEntryRestObject")


@_attrs_define
class RosterEntryRestObject:
    """
    Attributes:
        is_active_forty_man (bool | Unset):
        jersey_number (str | Unset): Jersey number that a player wears. Format: 16, 34, etc
        person (PersonRestObject | Unset):
        position (PositionRestObject | Unset):
        stats (Any | Unset):
    """

    is_active_forty_man: bool | Unset = UNSET
    jersey_number: str | Unset = UNSET
    person: PersonRestObject | Unset = UNSET
    position: PositionRestObject | Unset = UNSET
    stats: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject
        from ..models.position_rest_object import PositionRestObject

        is_active_forty_man = self.is_active_forty_man

        jersey_number = self.jersey_number

        person: dict[str, Any] | Unset = UNSET
        if not isinstance(self.person, Unset):
            person = self.person.to_dict()

        position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        stats = self.stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_active_forty_man is not UNSET:
            field_dict["isActiveFortyMan"] = is_active_forty_man
        if jersey_number is not UNSET:
            field_dict["jerseyNumber"] = jersey_number
        if person is not UNSET:
            field_dict["person"] = person
        if position is not UNSET:
            field_dict["position"] = position
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject
        from ..models.position_rest_object import PositionRestObject

        d = dict(src_dict)
        is_active_forty_man = d.pop("isActiveFortyMan", UNSET)

        jersey_number = d.pop("jerseyNumber", UNSET)

        _person = d.pop("person", UNSET)
        person: PersonRestObject | Unset
        if isinstance(_person, Unset):
            person = UNSET
        else:
            person = PersonRestObject.from_dict(_person)

        _position = d.pop("position", UNSET)
        position: PositionRestObject | Unset
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = PositionRestObject.from_dict(_position)

        stats = d.pop("stats", UNSET)

        roster_entry_rest_object = cls(
            is_active_forty_man=is_active_forty_man,
            jersey_number=jersey_number,
            person=person,
            position=position,
            stats=stats,
        )

        roster_entry_rest_object.additional_properties = d
        return roster_entry_rest_object

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
