from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameMetaDataRestObject")


@_attrs_define
class GameMetaDataRestObject:
    """
    Attributes:
        time_stamp (str | Unset): Use this parameter to return a snapshot of the data at the specified time. Format:
            YYYYMMDD_HHMMSS
        wait (int | Unset): Enter an integer for wait time
    """

    time_stamp: str | Unset = UNSET
    wait: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        time_stamp = self.time_stamp

        wait = self.wait

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time_stamp is not UNSET:
            field_dict["timeStamp"] = time_stamp
        if wait is not UNSET:
            field_dict["wait"] = wait

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        time_stamp = d.pop("timeStamp", UNSET)

        wait = d.pop("wait", UNSET)

        game_meta_data_rest_object = cls(
            time_stamp=time_stamp,
            wait=wait,
        )

        game_meta_data_rest_object.additional_properties = d
        return game_meta_data_rest_object

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
