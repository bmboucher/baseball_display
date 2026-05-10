from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseballHitDataRestObject")


@_attrs_define
class BaseballHitDataRestObject:
    """
    Attributes:
        hardness (str | Unset):
        hit_probability (float | Unset):
        is_barrel (bool | Unset):
        launch_angle (float | Unset):
        launch_speed (float | Unset):
        location (str | Unset):
        total_distance (float | Unset):
        trajectory (str | Unset):
    """

    hardness: str | Unset = UNSET
    hit_probability: float | Unset = UNSET
    is_barrel: bool | Unset = UNSET
    launch_angle: float | Unset = UNSET
    launch_speed: float | Unset = UNSET
    location: str | Unset = UNSET
    total_distance: float | Unset = UNSET
    trajectory: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hardness = self.hardness

        hit_probability = self.hit_probability

        is_barrel = self.is_barrel

        launch_angle = self.launch_angle

        launch_speed = self.launch_speed

        location = self.location

        total_distance = self.total_distance

        trajectory = self.trajectory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hardness is not UNSET:
            field_dict["hardness"] = hardness
        if hit_probability is not UNSET:
            field_dict["hitProbability"] = hit_probability
        if is_barrel is not UNSET:
            field_dict["isBarrel"] = is_barrel
        if launch_angle is not UNSET:
            field_dict["launchAngle"] = launch_angle
        if launch_speed is not UNSET:
            field_dict["launchSpeed"] = launch_speed
        if location is not UNSET:
            field_dict["location"] = location
        if total_distance is not UNSET:
            field_dict["totalDistance"] = total_distance
        if trajectory is not UNSET:
            field_dict["trajectory"] = trajectory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hardness = d.pop("hardness", UNSET)

        hit_probability = d.pop("hitProbability", UNSET)

        is_barrel = d.pop("isBarrel", UNSET)

        launch_angle = d.pop("launchAngle", UNSET)

        launch_speed = d.pop("launchSpeed", UNSET)

        location = d.pop("location", UNSET)

        total_distance = d.pop("totalDistance", UNSET)

        trajectory = d.pop("trajectory", UNSET)

        baseball_hit_data_rest_object = cls(
            hardness=hardness,
            hit_probability=hit_probability,
            is_barrel=is_barrel,
            launch_angle=launch_angle,
            launch_speed=launch_speed,
            location=location,
            total_distance=total_distance,
            trajectory=trajectory,
        )

        baseball_hit_data_rest_object.additional_properties = d
        return baseball_hit_data_rest_object

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
