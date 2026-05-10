from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hit_segment_rest_object import HitSegmentRestObject


T = TypeVar("T", bound="HomeRunDerbyBatterHitRestObject")


@_attrs_define
class HomeRunDerbyBatterHitRestObject:
    """
    Attributes:
        hit_data (HitSegmentRestObject | Unset):
        is_bonus_time (bool | Unset):
        is_home_run (bool | Unset):
        is_tie_breaker (bool | Unset):
        tie_breaker_num (int | Unset):
        time_remaining (str | Unset):
    """

    hit_data: HitSegmentRestObject | Unset = UNSET
    is_bonus_time: bool | Unset = UNSET
    is_home_run: bool | Unset = UNSET
    is_tie_breaker: bool | Unset = UNSET
    tie_breaker_num: int | Unset = UNSET
    time_remaining: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.hit_segment_rest_object import HitSegmentRestObject

        hit_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.hit_data, Unset):
            hit_data = self.hit_data.to_dict()

        is_bonus_time = self.is_bonus_time

        is_home_run = self.is_home_run

        is_tie_breaker = self.is_tie_breaker

        tie_breaker_num = self.tie_breaker_num

        time_remaining = self.time_remaining

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hit_data is not UNSET:
            field_dict["hitData"] = hit_data
        if is_bonus_time is not UNSET:
            field_dict["isBonusTime"] = is_bonus_time
        if is_home_run is not UNSET:
            field_dict["isHomeRun"] = is_home_run
        if is_tie_breaker is not UNSET:
            field_dict["isTieBreaker"] = is_tie_breaker
        if tie_breaker_num is not UNSET:
            field_dict["tieBreakerNum"] = tie_breaker_num
        if time_remaining is not UNSET:
            field_dict["timeRemaining"] = time_remaining

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hit_segment_rest_object import HitSegmentRestObject

        d = dict(src_dict)
        _hit_data = d.pop("hitData", UNSET)
        hit_data: HitSegmentRestObject | Unset
        if isinstance(_hit_data, Unset):
            hit_data = UNSET
        else:
            hit_data = HitSegmentRestObject.from_dict(_hit_data)

        is_bonus_time = d.pop("isBonusTime", UNSET)

        is_home_run = d.pop("isHomeRun", UNSET)

        is_tie_breaker = d.pop("isTieBreaker", UNSET)

        tie_breaker_num = d.pop("tieBreakerNum", UNSET)

        time_remaining = d.pop("timeRemaining", UNSET)

        home_run_derby_batter_hit_rest_object = cls(
            hit_data=hit_data,
            is_bonus_time=is_bonus_time,
            is_home_run=is_home_run,
            is_tie_breaker=is_tie_breaker,
            tie_breaker_num=tie_breaker_num,
            time_remaining=time_remaining,
        )

        home_run_derby_batter_hit_rest_object.additional_properties = d
        return home_run_derby_batter_hit_rest_object

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
