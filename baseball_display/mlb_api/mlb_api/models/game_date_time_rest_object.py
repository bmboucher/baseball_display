from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameDateTimeRestObject")


@_attrs_define
class GameDateTimeRestObject:
    """
    Attributes:
        date_time (datetime.datetime | Unset): Format: YYYY-MM-DDTHH:MM:SSZ
        end_date_time (datetime.datetime | Unset): Format: YYYY-MM-DDTHH:MM:SSZ
    """

    date_time: datetime.datetime | Unset = UNSET
    end_date_time: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_time: str | Unset = UNSET
        if not isinstance(self.date_time, Unset):
            date_time = self.date_time.isoformat()

        end_date_time: str | Unset = UNSET
        if not isinstance(self.end_date_time, Unset):
            end_date_time = self.end_date_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date_time is not UNSET:
            field_dict["dateTime"] = date_time
        if end_date_time is not UNSET:
            field_dict["endDateTime"] = end_date_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _date_time = d.pop("dateTime", UNSET)
        date_time: datetime.datetime | Unset
        if isinstance(_date_time, Unset):
            date_time = UNSET
        else:
            date_time = isoparse(_date_time)

        _end_date_time = d.pop("endDateTime", UNSET)
        end_date_time: datetime.datetime | Unset
        if isinstance(_end_date_time, Unset):
            end_date_time = UNSET
        else:
            end_date_time = isoparse(_end_date_time)

        game_date_time_rest_object = cls(
            date_time=date_time,
            end_date_time=end_date_time,
        )

        game_date_time_rest_object.additional_properties = d
        return game_date_time_rest_object

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
