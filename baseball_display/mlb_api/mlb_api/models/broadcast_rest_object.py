from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BroadcastRestObject")


@_attrs_define
class BroadcastRestObject:
    """
    Attributes:
        call_sign (str | Unset):
        home_away (str | Unset):
        id (int | Unset):
        is_national (bool | Unset):
        language (str | Unset):
        name (str | Unset): The name of the broadcast. Format: KWKW 1330, 95.7 FM The Game, etc
        site (str | Unset):
        source_url (int | Unset):
        type_ (str | Unset): The type of broadcast. Format: AM, FM, TV, etc
    """

    call_sign: str | Unset = UNSET
    home_away: str | Unset = UNSET
    id: int | Unset = UNSET
    is_national: bool | Unset = UNSET
    language: str | Unset = UNSET
    name: str | Unset = UNSET
    site: str | Unset = UNSET
    source_url: int | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_sign = self.call_sign

        home_away = self.home_away

        id = self.id

        is_national = self.is_national

        language = self.language

        name = self.name

        site = self.site

        source_url = self.source_url

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if call_sign is not UNSET:
            field_dict["callSign"] = call_sign
        if home_away is not UNSET:
            field_dict["homeAway"] = home_away
        if id is not UNSET:
            field_dict["id"] = id
        if is_national is not UNSET:
            field_dict["isNational"] = is_national
        if language is not UNSET:
            field_dict["language"] = language
        if name is not UNSET:
            field_dict["name"] = name
        if site is not UNSET:
            field_dict["site"] = site
        if source_url is not UNSET:
            field_dict["sourceUrl"] = source_url
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_sign = d.pop("callSign", UNSET)

        home_away = d.pop("homeAway", UNSET)

        id = d.pop("id", UNSET)

        is_national = d.pop("isNational", UNSET)

        language = d.pop("language", UNSET)

        name = d.pop("name", UNSET)

        site = d.pop("site", UNSET)

        source_url = d.pop("sourceUrl", UNSET)

        type_ = d.pop("type", UNSET)

        broadcast_rest_object = cls(
            call_sign=call_sign,
            home_away=home_away,
            id=id,
            is_national=is_national,
            language=language,
            name=name,
            site=site,
            source_url=source_url,
            type_=type_,
        )

        broadcast_rest_object.additional_properties = d
        return broadcast_rest_object

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
