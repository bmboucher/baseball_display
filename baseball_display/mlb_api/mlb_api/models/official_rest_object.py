from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="OfficialRestObject")


@_attrs_define
class OfficialRestObject:
    """
    Attributes:
        official (PersonRestObject | Unset):
        official_type (str | Unset):
    """

    official: PersonRestObject | Unset = UNSET
    official_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject

        official: dict[str, Any] | Unset = UNSET
        if not isinstance(self.official, Unset):
            official = self.official.to_dict()

        official_type = self.official_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if official is not UNSET:
            field_dict["official"] = official
        if official_type is not UNSET:
            field_dict["officialType"] = official_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        _official = d.pop("official", UNSET)
        official: PersonRestObject | Unset
        if isinstance(_official, Unset):
            official = UNSET
        else:
            official = PersonRestObject.from_dict(_official)

        official_type = d.pop("officialType", UNSET)

        official_rest_object = cls(
            official=official,
            official_type=official_type,
        )

        official_rest_object.additional_properties = d
        return official_rest_object

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
