from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stat_container_rest_object import StatContainerRestObject


T = TypeVar("T", bound="StatsRestObject")


@_attrs_define
class StatsRestObject:
    """
    Attributes:
        stats (list[StatContainerRestObject] | Unset):
    """

    stats: list[StatContainerRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.stat_container_rest_object import StatContainerRestObject

        stats: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = []
            for stats_item_data in self.stats:
                stats_item = stats_item_data.to_dict()
                stats.append(stats_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.stat_container_rest_object import StatContainerRestObject

        d = dict(src_dict)
        _stats = d.pop("stats", UNSET)
        stats: list[StatContainerRestObject] | Unset = UNSET
        if _stats is not UNSET:
            stats = []
            for stats_item_data in _stats:
                stats_item = StatContainerRestObject.from_dict(stats_item_data)

                stats.append(stats_item)

        stats_rest_object = cls(
            stats=stats,
        )

        stats_rest_object.additional_properties = d
        return stats_rest_object

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
