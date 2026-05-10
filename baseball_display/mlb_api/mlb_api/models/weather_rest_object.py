from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WeatherRestObject")


@_attrs_define
class WeatherRestObject:
    """
    Attributes:
        condition (str | Unset):
        temp (str | Unset):
        wind (str | Unset):
    """

    condition: str | Unset = UNSET
    temp: str | Unset = UNSET
    wind: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        condition = self.condition

        temp = self.temp

        wind = self.wind

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if condition is not UNSET:
            field_dict["condition"] = condition
        if temp is not UNSET:
            field_dict["temp"] = temp
        if wind is not UNSET:
            field_dict["wind"] = wind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        condition = d.pop("condition", UNSET)

        temp = d.pop("temp", UNSET)

        wind = d.pop("wind", UNSET)

        weather_rest_object = cls(
            condition=condition,
            temp=temp,
            wind=wind,
        )

        weather_rest_object.additional_properties = d
        return weather_rest_object

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
