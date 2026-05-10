from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LaunchDataRestObject")


@_attrs_define
class LaunchDataRestObject:
    """
    Attributes:
        angle (float | Unset):
        direction (float | Unset):
        speed (float | Unset):
        spin_axis (float | Unset):
        spin_rate (float | Unset):
    """

    angle: float | Unset = UNSET
    direction: float | Unset = UNSET
    speed: float | Unset = UNSET
    spin_axis: float | Unset = UNSET
    spin_rate: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        angle = self.angle

        direction = self.direction

        speed = self.speed

        spin_axis = self.spin_axis

        spin_rate = self.spin_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if angle is not UNSET:
            field_dict["angle"] = angle
        if direction is not UNSET:
            field_dict["direction"] = direction
        if speed is not UNSET:
            field_dict["speed"] = speed
        if spin_axis is not UNSET:
            field_dict["spinAxis"] = spin_axis
        if spin_rate is not UNSET:
            field_dict["spinRate"] = spin_rate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        angle = d.pop("angle", UNSET)

        direction = d.pop("direction", UNSET)

        speed = d.pop("speed", UNSET)

        spin_axis = d.pop("spinAxis", UNSET)

        spin_rate = d.pop("spinRate", UNSET)

        launch_data_rest_object = cls(
            angle=angle,
            direction=direction,
            speed=speed,
            spin_axis=spin_axis,
            spin_rate=spin_rate,
        )

        launch_data_rest_object.additional_properties = d
        return launch_data_rest_object

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
