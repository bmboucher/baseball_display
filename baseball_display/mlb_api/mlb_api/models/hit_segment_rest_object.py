from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hit_trajectory_data_rest_object import HitTrajectoryDataRestObject
    from ..models.launch_data_rest_object import LaunchDataRestObject
    from ..models.start_end_data_rest_object import StartEndDataRestObject


T = TypeVar("T", bound="HitSegmentRestObject")


@_attrs_define
class HitSegmentRestObject:
    """
    Attributes:
        landing_data (StartEndDataRestObject | Unset):
        last_measured_data (StartEndDataRestObject | Unset):
        launch_data (LaunchDataRestObject | Unset):
        reduced_confidence (list[str] | Unset):
        trajectory_data (HitTrajectoryDataRestObject | Unset):
    """

    landing_data: StartEndDataRestObject | Unset = UNSET
    last_measured_data: StartEndDataRestObject | Unset = UNSET
    launch_data: LaunchDataRestObject | Unset = UNSET
    reduced_confidence: list[str] | Unset = UNSET
    trajectory_data: HitTrajectoryDataRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.hit_trajectory_data_rest_object import HitTrajectoryDataRestObject
        from ..models.launch_data_rest_object import LaunchDataRestObject
        from ..models.start_end_data_rest_object import StartEndDataRestObject

        landing_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.landing_data, Unset):
            landing_data = self.landing_data.to_dict()

        last_measured_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.last_measured_data, Unset):
            last_measured_data = self.last_measured_data.to_dict()

        launch_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.launch_data, Unset):
            launch_data = self.launch_data.to_dict()

        reduced_confidence: list[str] | Unset = UNSET
        if not isinstance(self.reduced_confidence, Unset):
            reduced_confidence = self.reduced_confidence

        trajectory_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.trajectory_data, Unset):
            trajectory_data = self.trajectory_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if landing_data is not UNSET:
            field_dict["landingData"] = landing_data
        if last_measured_data is not UNSET:
            field_dict["lastMeasuredData"] = last_measured_data
        if launch_data is not UNSET:
            field_dict["launchData"] = launch_data
        if reduced_confidence is not UNSET:
            field_dict["reducedConfidence"] = reduced_confidence
        if trajectory_data is not UNSET:
            field_dict["trajectoryData"] = trajectory_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hit_trajectory_data_rest_object import HitTrajectoryDataRestObject
        from ..models.launch_data_rest_object import LaunchDataRestObject
        from ..models.start_end_data_rest_object import StartEndDataRestObject

        d = dict(src_dict)
        _landing_data = d.pop("landingData", UNSET)
        landing_data: StartEndDataRestObject | Unset
        if isinstance(_landing_data, Unset):
            landing_data = UNSET
        else:
            landing_data = StartEndDataRestObject.from_dict(_landing_data)

        _last_measured_data = d.pop("lastMeasuredData", UNSET)
        last_measured_data: StartEndDataRestObject | Unset
        if isinstance(_last_measured_data, Unset):
            last_measured_data = UNSET
        else:
            last_measured_data = StartEndDataRestObject.from_dict(_last_measured_data)

        _launch_data = d.pop("launchData", UNSET)
        launch_data: LaunchDataRestObject | Unset
        if isinstance(_launch_data, Unset):
            launch_data = UNSET
        else:
            launch_data = LaunchDataRestObject.from_dict(_launch_data)

        reduced_confidence = cast(list[str], d.pop("reducedConfidence", UNSET))

        _trajectory_data = d.pop("trajectoryData", UNSET)
        trajectory_data: HitTrajectoryDataRestObject | Unset
        if isinstance(_trajectory_data, Unset):
            trajectory_data = UNSET
        else:
            trajectory_data = HitTrajectoryDataRestObject.from_dict(_trajectory_data)

        hit_segment_rest_object = cls(
            landing_data=landing_data,
            last_measured_data=last_measured_data,
            launch_data=launch_data,
            reduced_confidence=reduced_confidence,
            trajectory_data=trajectory_data,
        )

        hit_segment_rest_object.additional_properties = d
        return hit_segment_rest_object

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
