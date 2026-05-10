from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OtherNamesRestObject")


@_attrs_define
class OtherNamesRestObject:
    """
    Attributes:
        first_initial_last_name (str | Unset):
        last_first_name (str | Unset):
        last_name_first_initial (str | Unset):
        phonetic_name (str | Unset):
        slug (str | Unset):
    """

    first_initial_last_name: str | Unset = UNSET
    last_first_name: str | Unset = UNSET
    last_name_first_initial: str | Unset = UNSET
    phonetic_name: str | Unset = UNSET
    slug: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        first_initial_last_name = self.first_initial_last_name

        last_first_name = self.last_first_name

        last_name_first_initial = self.last_name_first_initial

        phonetic_name = self.phonetic_name

        slug = self.slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_initial_last_name is not UNSET:
            field_dict["firstInitialLastName"] = first_initial_last_name
        if last_first_name is not UNSET:
            field_dict["lastFirstName"] = last_first_name
        if last_name_first_initial is not UNSET:
            field_dict["lastNameFirstInitial"] = last_name_first_initial
        if phonetic_name is not UNSET:
            field_dict["phoneticName"] = phonetic_name
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        first_initial_last_name = d.pop("firstInitialLastName", UNSET)

        last_first_name = d.pop("lastFirstName", UNSET)

        last_name_first_initial = d.pop("lastNameFirstInitial", UNSET)

        phonetic_name = d.pop("phoneticName", UNSET)

        slug = d.pop("slug", UNSET)

        other_names_rest_object = cls(
            first_initial_last_name=first_initial_last_name,
            last_first_name=last_first_name,
            last_name_first_initial=last_name_first_initial,
            phonetic_name=phonetic_name,
            slug=slug,
        )

        other_names_rest_object.additional_properties = d
        return other_names_rest_object

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
