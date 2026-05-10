from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sport_rest_object import SportRestObject


T = TypeVar("T", bound="SportsRestObject")


@_attrs_define
class SportsRestObject:
    """
    Attributes:
        sports (list[SportRestObject] | Unset):
    """

    sports: list[SportRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sport_rest_object import SportRestObject

        sports: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sports, Unset):
            sports = []
            for sports_item_data in self.sports:
                sports_item = sports_item_data.to_dict()
                sports.append(sports_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sports is not UNSET:
            field_dict["sports"] = sports

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sport_rest_object import SportRestObject

        d = dict(src_dict)
        _sports = d.pop("sports", UNSET)
        sports: list[SportRestObject] | Unset = UNSET
        if _sports is not UNSET:
            sports = []
            for sports_item_data in _sports:
                sports_item = SportRestObject.from_dict(sports_item_data)

                sports.append(sports_item)

        sports_rest_object = cls(
            sports=sports,
        )

        sports_rest_object.additional_properties = d
        return sports_rest_object

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
