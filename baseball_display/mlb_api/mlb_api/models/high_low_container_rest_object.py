from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.baseball_stats_type_rest_object import BaseballStatsTypeRestObject


T = TypeVar("T", bound="HighLowContainerRestObject")


@_attrs_define
class HighLowContainerRestObject:
    """
    Attributes:
        combined_stats (bool | Unset):
        season (str | Unset):
        sort_stat (BaseballStatsTypeRestObject | Unset):
    """

    combined_stats: bool | Unset = UNSET
    season: str | Unset = UNSET
    sort_stat: BaseballStatsTypeRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.baseball_stats_type_rest_object import BaseballStatsTypeRestObject

        combined_stats = self.combined_stats

        season = self.season

        sort_stat: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sort_stat, Unset):
            sort_stat = self.sort_stat.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if combined_stats is not UNSET:
            field_dict["combinedStats"] = combined_stats
        if season is not UNSET:
            field_dict["season"] = season
        if sort_stat is not UNSET:
            field_dict["sortStat"] = sort_stat

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseball_stats_type_rest_object import BaseballStatsTypeRestObject

        d = dict(src_dict)
        combined_stats = d.pop("combinedStats", UNSET)

        season = d.pop("season", UNSET)

        _sort_stat = d.pop("sortStat", UNSET)
        sort_stat: BaseballStatsTypeRestObject | Unset
        if isinstance(_sort_stat, Unset):
            sort_stat = UNSET
        else:
            sort_stat = BaseballStatsTypeRestObject.from_dict(_sort_stat)

        high_low_container_rest_object = cls(
            combined_stats=combined_stats,
            season=season,
            sort_stat=sort_stat,
        )

        high_low_container_rest_object.additional_properties = d
        return high_low_container_rest_object

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
