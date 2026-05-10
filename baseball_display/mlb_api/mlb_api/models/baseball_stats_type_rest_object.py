from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseballStatsTypeRestObject")


@_attrs_define
class BaseballStatsTypeRestObject:
    """
    Attributes:
        is_counting (bool | Unset):
        label (str | Unset):
        lookup_param (str | Unset):
        name (str | Unset):
        org_types (list[str] | Unset):
        stat_groups (list[str] | Unset):
    """

    is_counting: bool | Unset = UNSET
    label: str | Unset = UNSET
    lookup_param: str | Unset = UNSET
    name: str | Unset = UNSET
    org_types: list[str] | Unset = UNSET
    stat_groups: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_counting = self.is_counting

        label = self.label

        lookup_param = self.lookup_param

        name = self.name

        org_types: list[str] | Unset = UNSET
        if not isinstance(self.org_types, Unset):
            org_types = self.org_types

        stat_groups: list[str] | Unset = UNSET
        if not isinstance(self.stat_groups, Unset):
            stat_groups = self.stat_groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_counting is not UNSET:
            field_dict["isCounting"] = is_counting
        if label is not UNSET:
            field_dict["label"] = label
        if lookup_param is not UNSET:
            field_dict["lookupParam"] = lookup_param
        if name is not UNSET:
            field_dict["name"] = name
        if org_types is not UNSET:
            field_dict["orgTypes"] = org_types
        if stat_groups is not UNSET:
            field_dict["statGroups"] = stat_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_counting = d.pop("isCounting", UNSET)

        label = d.pop("label", UNSET)

        lookup_param = d.pop("lookupParam", UNSET)

        name = d.pop("name", UNSET)

        org_types = cast(list[str], d.pop("orgTypes", UNSET))

        stat_groups = cast(list[str], d.pop("statGroups", UNSET))

        baseball_stats_type_rest_object = cls(
            is_counting=is_counting,
            label=label,
            lookup_param=lookup_param,
            name=name,
            org_types=org_types,
            stat_groups=stat_groups,
        )

        baseball_stats_type_rest_object.additional_properties = d
        return baseball_stats_type_rest_object

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
