from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.play_rest_object import PlayRestObject


T = TypeVar("T", bound="PlayByPlayRestObject")


@_attrs_define
class PlayByPlayRestObject:
    """
    Attributes:
        plays (list[PlayRestObject] | Unset): Includes all details about all the plays of a game
    """

    plays: list[PlayRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.play_rest_object import PlayRestObject

        plays: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.plays, Unset):
            plays = []
            for plays_item_data in self.plays:
                plays_item = plays_item_data.to_dict()
                plays.append(plays_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plays is not UNSET:
            field_dict["plays"] = plays

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.play_rest_object import PlayRestObject

        d = dict(src_dict)
        _plays = d.pop("plays", UNSET)
        plays: list[PlayRestObject] | Unset = UNSET
        if _plays is not UNSET:
            plays = []
            for plays_item_data in _plays:
                plays_item = PlayRestObject.from_dict(plays_item_data)

                plays.append(plays_item)

        play_by_play_rest_object = cls(
            plays=plays,
        )

        play_by_play_rest_object.additional_properties = d
        return play_by_play_rest_object

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
