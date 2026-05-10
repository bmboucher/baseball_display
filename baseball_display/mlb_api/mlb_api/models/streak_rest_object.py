from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StreakRestObject")


@_attrs_define
class StreakRestObject:
    """
    Attributes:
        streak_code (str | Unset):
        streak_number (int | Unset):
        streak_type (str | Unset):
    """

    streak_code: str | Unset = UNSET
    streak_number: int | Unset = UNSET
    streak_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        streak_code = self.streak_code

        streak_number = self.streak_number

        streak_type = self.streak_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if streak_code is not UNSET:
            field_dict["streakCode"] = streak_code
        if streak_number is not UNSET:
            field_dict["streakNumber"] = streak_number
        if streak_type is not UNSET:
            field_dict["streakType"] = streak_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        streak_code = d.pop("streakCode", UNSET)

        streak_number = d.pop("streakNumber", UNSET)

        streak_type = d.pop("streakType", UNSET)

        streak_rest_object = cls(
            streak_code=streak_code,
            streak_number=streak_number,
            streak_type=streak_type,
        )

        streak_rest_object.additional_properties = d
        return streak_rest_object

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
