from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StartEndDataRestObject")


@_attrs_define
class StartEndDataRestObject:
    """
    Attributes:
        bearing (float | Unset):
        distance (float | Unset):
        speed (float | Unset):
    """

    bearing: float | Unset = UNSET
    distance: float | Unset = UNSET
    speed: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bearing = self.bearing

        distance = self.distance

        speed = self.speed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bearing is not UNSET:
            field_dict["bearing"] = bearing
        if distance is not UNSET:
            field_dict["distance"] = distance
        if speed is not UNSET:
            field_dict["speed"] = speed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bearing = d.pop("bearing", UNSET)

        distance = d.pop("distance", UNSET)

        speed = d.pop("speed", UNSET)

        start_end_data_rest_object = cls(
            bearing=bearing,
            distance=distance,
            speed=speed,
        )

        start_end_data_rest_object.additional_properties = d
        return start_end_data_rest_object

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
