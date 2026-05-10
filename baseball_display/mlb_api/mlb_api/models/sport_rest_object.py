from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SportRestObject")


@_attrs_define
class SportRestObject:
    """
    Attributes:
        abbreviation (str | Unset): Shortened version of short name. Format: ALE, SFG
        code (str | Unset):
        device_properties (Any | Unset):
        id (int | Unset): Top level organization of a sport
        link (str | Unset): Link to full resource
        name (str | Unset): Name of a sport's league. Format: Major League Baseball
    """

    abbreviation: str | Unset = UNSET
    code: str | Unset = UNSET
    device_properties: Any | Unset = UNSET
    id: int | Unset = UNSET
    link: str | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        abbreviation = self.abbreviation

        code = self.code

        device_properties = self.device_properties

        id = self.id

        link = self.link

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if code is not UNSET:
            field_dict["code"] = code
        if device_properties is not UNSET:
            field_dict["deviceProperties"] = device_properties
        if id is not UNSET:
            field_dict["id"] = id
        if link is not UNSET:
            field_dict["link"] = link
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        abbreviation = d.pop("abbreviation", UNSET)

        code = d.pop("code", UNSET)

        device_properties = d.pop("deviceProperties", UNSET)

        id = d.pop("id", UNSET)

        link = d.pop("link", UNSET)

        name = d.pop("name", UNSET)

        sport_rest_object = cls(
            abbreviation=abbreviation,
            code=code,
            device_properties=device_properties,
            id=id,
            link=link,
            name=name,
        )

        sport_rest_object.additional_properties = d
        return sport_rest_object

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
