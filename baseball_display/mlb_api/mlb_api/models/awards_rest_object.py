from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_rest_object import AwardRestObject


T = TypeVar("T", bound="AwardsRestObject")


@_attrs_define
class AwardsRestObject:
    """
    Attributes:
        awards (list[AwardRestObject] | Unset):
    """

    awards: list[AwardRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_rest_object import AwardRestObject

        awards: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.awards, Unset):
            awards = []
            for awards_item_data in self.awards:
                awards_item = awards_item_data.to_dict()
                awards.append(awards_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if awards is not UNSET:
            field_dict["awards"] = awards

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_rest_object import AwardRestObject

        d = dict(src_dict)
        _awards = d.pop("awards", UNSET)
        awards: list[AwardRestObject] | Unset = UNSET
        if _awards is not UNSET:
            awards = []
            for awards_item_data in _awards:
                awards_item = AwardRestObject.from_dict(awards_item_data)

                awards.append(awards_item)

        awards_rest_object = cls(
            awards=awards,
        )

        awards_rest_object.additional_properties = d
        return awards_rest_object

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
