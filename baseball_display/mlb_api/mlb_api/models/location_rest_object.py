from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationRestObject")


@_attrs_define
class LocationRestObject:
    """
    Attributes:
        state (str | Unset): State where the venue is located. Format: Ohio
        state_abbrev (str | Unset): State abbrevation where the venue is located. Format: OH
    """

    state: str | Unset = UNSET
    state_abbrev: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        state_abbrev = self.state_abbrev

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if state_abbrev is not UNSET:
            field_dict["stateAbbrev"] = state_abbrev

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state", UNSET)

        state_abbrev = d.pop("stateAbbrev", UNSET)

        location_rest_object = cls(
            state=state,
            state_abbrev=state_abbrev,
        )

        location_rest_object.additional_properties = d
        return location_rest_object

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
