from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.official_rest_object import OfficialRestObject


T = TypeVar("T", bound="Boxscore")


@_attrs_define
class Boxscore:
    """
    Attributes:
        officials (list[OfficialRestObject] | Unset):
    """

    officials: list[OfficialRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.official_rest_object import OfficialRestObject

        officials: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.officials, Unset):
            officials = []
            for officials_item_data in self.officials:
                officials_item = officials_item_data.to_dict()
                officials.append(officials_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if officials is not UNSET:
            field_dict["officials"] = officials

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.official_rest_object import OfficialRestObject

        d = dict(src_dict)
        _officials = d.pop("officials", UNSET)
        officials: list[OfficialRestObject] | Unset = UNSET
        if _officials is not UNSET:
            officials = []
            for officials_item_data in _officials:
                officials_item = OfficialRestObject.from_dict(officials_item_data)

                officials.append(officials_item)

        boxscore = cls(
            officials=officials,
        )

        boxscore.additional_properties = d
        return boxscore

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
