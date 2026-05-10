from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conference_rest_object import ConferenceRestObject


T = TypeVar("T", bound="ConferencesRestObject")


@_attrs_define
class ConferencesRestObject:
    """
    Attributes:
        conferences (list[ConferenceRestObject] | Unset):
    """

    conferences: list[ConferenceRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conference_rest_object import ConferenceRestObject

        conferences: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conferences, Unset):
            conferences = []
            for conferences_item_data in self.conferences:
                conferences_item = conferences_item_data.to_dict()
                conferences.append(conferences_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conferences is not UNSET:
            field_dict["conferences"] = conferences

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conference_rest_object import ConferenceRestObject

        d = dict(src_dict)
        _conferences = d.pop("conferences", UNSET)
        conferences: list[ConferenceRestObject] | Unset = UNSET
        if _conferences is not UNSET:
            conferences = []
            for conferences_item_data in _conferences:
                conferences_item = ConferenceRestObject.from_dict(conferences_item_data)

                conferences.append(conferences_item)

        conferences_rest_object = cls(
            conferences=conferences,
        )

        conferences_rest_object.additional_properties = d
        return conferences_rest_object

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
