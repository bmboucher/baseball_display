from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameDataGameRestObject")


@_attrs_define
class GameDataGameRestObject:
    """
    Attributes:
        pk (int | Unset): Unique Primary Key Representing a Game
        type_ (str | Unset): Type of Game. Available types in /api/v1/gameTypes
    """

    pk: int | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pk = self.pk

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pk is not UNSET:
            field_dict["pk"] = pk
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pk = d.pop("pk", UNSET)

        type_ = d.pop("type", UNSET)

        game_data_game_rest_object = cls(
            pk=pk,
            type_=type_,
        )

        game_data_game_rest_object.additional_properties = d
        return game_data_game_rest_object

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
