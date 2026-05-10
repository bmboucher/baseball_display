from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.season_rest_object import SeasonRestObject


T = TypeVar("T", bound="SeasonsRestObject")


@_attrs_define
class SeasonsRestObject:
    """
    Attributes:
        seasons (list[SeasonRestObject] | Unset):
    """

    seasons: list[SeasonRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.season_rest_object import SeasonRestObject

        seasons: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.seasons, Unset):
            seasons = []
            for seasons_item_data in self.seasons:
                seasons_item = seasons_item_data.to_dict()
                seasons.append(seasons_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if seasons is not UNSET:
            field_dict["seasons"] = seasons

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.season_rest_object import SeasonRestObject

        d = dict(src_dict)
        _seasons = d.pop("seasons", UNSET)
        seasons: list[SeasonRestObject] | Unset = UNSET
        if _seasons is not UNSET:
            seasons = []
            for seasons_item_data in _seasons:
                seasons_item = SeasonRestObject.from_dict(seasons_item_data)

                seasons.append(seasons_item)

        seasons_rest_object = cls(
            seasons=seasons,
        )

        seasons_rest_object.additional_properties = d
        return seasons_rest_object

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
