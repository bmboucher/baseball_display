from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameInfoRestObject")


@_attrs_define
class GameInfoRestObject:
    """
    Attributes:
        attendance (int | Unset): Number of fans at the stadium as recorded by the club.
        delay_duration_minutes (int | Unset): Amount of timet he game was delayed (in seconds).
        first_pitch (datetime.datetime | Unset): Time that the first pitch was thrown.
        game_duration_minutes (int | Unset): Amount of time the game lasted (in seconds).
    """

    attendance: int | Unset = UNSET
    delay_duration_minutes: int | Unset = UNSET
    first_pitch: datetime.datetime | Unset = UNSET
    game_duration_minutes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attendance = self.attendance

        delay_duration_minutes = self.delay_duration_minutes

        first_pitch: str | Unset = UNSET
        if not isinstance(self.first_pitch, Unset):
            first_pitch = self.first_pitch.isoformat()

        game_duration_minutes = self.game_duration_minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attendance is not UNSET:
            field_dict["attendance"] = attendance
        if delay_duration_minutes is not UNSET:
            field_dict["delayDurationMinutes"] = delay_duration_minutes
        if first_pitch is not UNSET:
            field_dict["firstPitch"] = first_pitch
        if game_duration_minutes is not UNSET:
            field_dict["gameDurationMinutes"] = game_duration_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attendance = d.pop("attendance", UNSET)

        delay_duration_minutes = d.pop("delayDurationMinutes", UNSET)

        _first_pitch = d.pop("firstPitch", UNSET)
        first_pitch: datetime.datetime | Unset
        if isinstance(_first_pitch, Unset):
            first_pitch = UNSET
        else:
            first_pitch = isoparse(_first_pitch)

        game_duration_minutes = d.pop("gameDurationMinutes", UNSET)

        game_info_rest_object = cls(
            attendance=attendance,
            delay_duration_minutes=delay_duration_minutes,
            first_pitch=first_pitch,
            game_duration_minutes=game_duration_minutes,
        )

        game_info_rest_object.additional_properties = d
        return game_info_rest_object

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
