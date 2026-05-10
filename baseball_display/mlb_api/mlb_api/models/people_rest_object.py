from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="PeopleRestObject")


@_attrs_define
class PeopleRestObject:
    """
    Attributes:
        people (list[PersonRestObject] | Unset):
    """

    people: list[PersonRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject

        people: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.people, Unset):
            people = []
            for people_item_data in self.people:
                people_item = people_item_data.to_dict()
                people.append(people_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if people is not UNSET:
            field_dict["people"] = people

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        _people = d.pop("people", UNSET)
        people: list[PersonRestObject] | Unset = UNSET
        if _people is not UNSET:
            people = []
            for people_item_data in _people:
                people_item = PersonRestObject.from_dict(people_item_data)

                people.append(people_item)

        people_rest_object = cls(
            people=people,
        )

        people_rest_object.additional_properties = d
        return people_rest_object

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
