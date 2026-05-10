from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionRestObject")


@_attrs_define
class PositionRestObject:
    """
    Attributes:
        abbreviation (str | Unset): Position abbreviation. Format: SS, P, 1B, etc
        code (str | Unset): Position number. Format: 1, 2, 3, etc
        name (str | Unset): Position name. Format: First base, Shortstop, Pitcher, etc
        type_ (str | Unset): Position type. Format: Infielder, Pitcher, etc
    """

    abbreviation: str | Unset = UNSET
    code: str | Unset = UNSET
    name: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        abbreviation = self.abbreviation

        code = self.code

        name = self.name

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if code is not UNSET:
            field_dict["code"] = code
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        abbreviation = d.pop("abbreviation", UNSET)

        code = d.pop("code", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        position_rest_object = cls(
            abbreviation=abbreviation,
            code=code,
            name=name,
            type_=type_,
        )

        position_rest_object.additional_properties = d
        return position_rest_object

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
