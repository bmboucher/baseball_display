from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EducationRestObject")


@_attrs_define
class EducationRestObject:
    """
    Attributes:
        colleges (list[Any] | Unset): The player's college(s)
        highschools (list[Any] | Unset): The player's highschool(s)
    """

    colleges: list[Any] | Unset = UNSET
    highschools: list[Any] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        colleges: list[Any] | Unset = UNSET
        if not isinstance(self.colleges, Unset):
            colleges = self.colleges

        highschools: list[Any] | Unset = UNSET
        if not isinstance(self.highschools, Unset):
            highschools = self.highschools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if colleges is not UNSET:
            field_dict["colleges"] = colleges
        if highschools is not UNSET:
            field_dict["highschools"] = highschools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        colleges = cast(list[Any], d.pop("colleges", UNSET))

        highschools = cast(list[Any], d.pop("highschools", UNSET))

        education_rest_object = cls(
            colleges=colleges,
            highschools=highschools,
        )

        education_rest_object.additional_properties = d
        return education_rest_object

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
