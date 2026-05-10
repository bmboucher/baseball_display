from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.division_rest_object import DivisionRestObject


T = TypeVar("T", bound="DivisionsRestObject")


@_attrs_define
class DivisionsRestObject:
    """
    Attributes:
        divisions (list[DivisionRestObject] | Unset):
    """

    divisions: list[DivisionRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.division_rest_object import DivisionRestObject

        divisions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.divisions, Unset):
            divisions = []
            for divisions_item_data in self.divisions:
                divisions_item = divisions_item_data.to_dict()
                divisions.append(divisions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if divisions is not UNSET:
            field_dict["divisions"] = divisions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.division_rest_object import DivisionRestObject

        d = dict(src_dict)
        _divisions = d.pop("divisions", UNSET)
        divisions: list[DivisionRestObject] | Unset = UNSET
        if _divisions is not UNSET:
            divisions = []
            for divisions_item_data in _divisions:
                divisions_item = DivisionRestObject.from_dict(divisions_item_data)

                divisions.append(divisions_item)

        divisions_rest_object = cls(
            divisions=divisions,
        )

        divisions_rest_object.additional_properties = d
        return divisions_rest_object

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
