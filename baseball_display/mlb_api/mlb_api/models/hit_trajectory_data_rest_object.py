from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coordinates_rest_object import CoordinatesRestObject


T = TypeVar("T", bound="HitTrajectoryDataRestObject")


@_attrs_define
class HitTrajectoryDataRestObject:
    """
    Attributes:
        hit_position_at_110_feet (CoordinatesRestObject | Unset):
        max_height_position (CoordinatesRestObject | Unset):
        measured_time_interval (list[float] | Unset):
        reduced_confidence (list[str] | Unset):
        trajectory_polynomial_x (list[float] | Unset):
        trajectory_polynomial_y (list[float] | Unset):
        trajectory_polynomial_z (list[float] | Unset):
        valid_time_interval (list[float] | Unset):
    """

    hit_position_at_110_feet: CoordinatesRestObject | Unset = UNSET
    max_height_position: CoordinatesRestObject | Unset = UNSET
    measured_time_interval: list[float] | Unset = UNSET
    reduced_confidence: list[str] | Unset = UNSET
    trajectory_polynomial_x: list[float] | Unset = UNSET
    trajectory_polynomial_y: list[float] | Unset = UNSET
    trajectory_polynomial_z: list[float] | Unset = UNSET
    valid_time_interval: list[float] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.coordinates_rest_object import CoordinatesRestObject

        hit_position_at_110_feet: dict[str, Any] | Unset = UNSET
        if not isinstance(self.hit_position_at_110_feet, Unset):
            hit_position_at_110_feet = self.hit_position_at_110_feet.to_dict()

        max_height_position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.max_height_position, Unset):
            max_height_position = self.max_height_position.to_dict()

        measured_time_interval: list[float] | Unset = UNSET
        if not isinstance(self.measured_time_interval, Unset):
            measured_time_interval = self.measured_time_interval

        reduced_confidence: list[str] | Unset = UNSET
        if not isinstance(self.reduced_confidence, Unset):
            reduced_confidence = self.reduced_confidence

        trajectory_polynomial_x: list[float] | Unset = UNSET
        if not isinstance(self.trajectory_polynomial_x, Unset):
            trajectory_polynomial_x = self.trajectory_polynomial_x

        trajectory_polynomial_y: list[float] | Unset = UNSET
        if not isinstance(self.trajectory_polynomial_y, Unset):
            trajectory_polynomial_y = self.trajectory_polynomial_y

        trajectory_polynomial_z: list[float] | Unset = UNSET
        if not isinstance(self.trajectory_polynomial_z, Unset):
            trajectory_polynomial_z = self.trajectory_polynomial_z

        valid_time_interval: list[float] | Unset = UNSET
        if not isinstance(self.valid_time_interval, Unset):
            valid_time_interval = self.valid_time_interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hit_position_at_110_feet is not UNSET:
            field_dict["hitPositionAt110Feet"] = hit_position_at_110_feet
        if max_height_position is not UNSET:
            field_dict["maxHeightPosition"] = max_height_position
        if measured_time_interval is not UNSET:
            field_dict["measuredTimeInterval"] = measured_time_interval
        if reduced_confidence is not UNSET:
            field_dict["reducedConfidence"] = reduced_confidence
        if trajectory_polynomial_x is not UNSET:
            field_dict["trajectoryPolynomialX"] = trajectory_polynomial_x
        if trajectory_polynomial_y is not UNSET:
            field_dict["trajectoryPolynomialY"] = trajectory_polynomial_y
        if trajectory_polynomial_z is not UNSET:
            field_dict["trajectoryPolynomialZ"] = trajectory_polynomial_z
        if valid_time_interval is not UNSET:
            field_dict["validTimeInterval"] = valid_time_interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.coordinates_rest_object import CoordinatesRestObject

        d = dict(src_dict)
        _hit_position_at_110_feet = d.pop("hitPositionAt110Feet", UNSET)
        hit_position_at_110_feet: CoordinatesRestObject | Unset
        if isinstance(_hit_position_at_110_feet, Unset):
            hit_position_at_110_feet = UNSET
        else:
            hit_position_at_110_feet = CoordinatesRestObject.from_dict(
                _hit_position_at_110_feet
            )

        _max_height_position = d.pop("maxHeightPosition", UNSET)
        max_height_position: CoordinatesRestObject | Unset
        if isinstance(_max_height_position, Unset):
            max_height_position = UNSET
        else:
            max_height_position = CoordinatesRestObject.from_dict(_max_height_position)

        measured_time_interval = cast(list[float], d.pop("measuredTimeInterval", UNSET))

        reduced_confidence = cast(list[str], d.pop("reducedConfidence", UNSET))

        trajectory_polynomial_x = cast(
            list[float], d.pop("trajectoryPolynomialX", UNSET)
        )

        trajectory_polynomial_y = cast(
            list[float], d.pop("trajectoryPolynomialY", UNSET)
        )

        trajectory_polynomial_z = cast(
            list[float], d.pop("trajectoryPolynomialZ", UNSET)
        )

        valid_time_interval = cast(list[float], d.pop("validTimeInterval", UNSET))

        hit_trajectory_data_rest_object = cls(
            hit_position_at_110_feet=hit_position_at_110_feet,
            max_height_position=max_height_position,
            measured_time_interval=measured_time_interval,
            reduced_confidence=reduced_confidence,
            trajectory_polynomial_x=trajectory_polynomial_x,
            trajectory_polynomial_y=trajectory_polynomial_y,
            trajectory_polynomial_z=trajectory_polynomial_z,
            valid_time_interval=valid_time_interval,
        )

        hit_trajectory_data_rest_object.additional_properties = d
        return hit_trajectory_data_rest_object

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
