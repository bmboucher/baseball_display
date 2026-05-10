from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StolenBaseProbabilityRestObject")


@_attrs_define
class StolenBaseProbabilityRestObject:
    """
    Attributes:
        end_color (str | Unset):
        foot_markers (list[Any] | Unset):
        start_color (str | Unset):
    """

    end_color: str | Unset = UNSET
    foot_markers: list[Any] | Unset = UNSET
    start_color: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_color = self.end_color

        foot_markers: list[Any] | Unset = UNSET
        if not isinstance(self.foot_markers, Unset):
            foot_markers = self.foot_markers

        start_color = self.start_color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end_color is not UNSET:
            field_dict["endColor"] = end_color
        if foot_markers is not UNSET:
            field_dict["footMarkers"] = foot_markers
        if start_color is not UNSET:
            field_dict["startColor"] = start_color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_color = d.pop("endColor", UNSET)

        foot_markers = cast(list[Any], d.pop("footMarkers", UNSET))

        start_color = d.pop("startColor", UNSET)

        stolen_base_probability_rest_object = cls(
            end_color=end_color,
            foot_markers=foot_markers,
            start_color=start_color,
        )

        stolen_base_probability_rest_object.additional_properties = d
        return stolen_base_probability_rest_object

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
