from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromotionRestObject")


@_attrs_define
class PromotionRestObject:
    """
    Attributes:
        alt_page_url (str | Unset):
        description (str | Unset):
        display_if_past (bool | Unset):
        distribution (str | Unset):
        image_url (str | Unset):
        name (str | Unset):
        offer_id (int | Unset):
        offer_type (str | Unset):
        order (int | Unset):
        other (str | Unset):
        presented_by (str | Unset):
        sort_key (str | Unset):
        team_id (int | Unset):
        thumbnail_url (str | Unset):
        tlink (str | Unset):
    """

    alt_page_url: str | Unset = UNSET
    description: str | Unset = UNSET
    display_if_past: bool | Unset = UNSET
    distribution: str | Unset = UNSET
    image_url: str | Unset = UNSET
    name: str | Unset = UNSET
    offer_id: int | Unset = UNSET
    offer_type: str | Unset = UNSET
    order: int | Unset = UNSET
    other: str | Unset = UNSET
    presented_by: str | Unset = UNSET
    sort_key: str | Unset = UNSET
    team_id: int | Unset = UNSET
    thumbnail_url: str | Unset = UNSET
    tlink: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alt_page_url = self.alt_page_url

        description = self.description

        display_if_past = self.display_if_past

        distribution = self.distribution

        image_url = self.image_url

        name = self.name

        offer_id = self.offer_id

        offer_type = self.offer_type

        order = self.order

        other = self.other

        presented_by = self.presented_by

        sort_key = self.sort_key

        team_id = self.team_id

        thumbnail_url = self.thumbnail_url

        tlink = self.tlink

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alt_page_url is not UNSET:
            field_dict["altPageUrl"] = alt_page_url
        if description is not UNSET:
            field_dict["description"] = description
        if display_if_past is not UNSET:
            field_dict["displayIfPast"] = display_if_past
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if name is not UNSET:
            field_dict["name"] = name
        if offer_id is not UNSET:
            field_dict["offerId"] = offer_id
        if offer_type is not UNSET:
            field_dict["offerType"] = offer_type
        if order is not UNSET:
            field_dict["order"] = order
        if other is not UNSET:
            field_dict["other"] = other
        if presented_by is not UNSET:
            field_dict["presentedBy"] = presented_by
        if sort_key is not UNSET:
            field_dict["sortKey"] = sort_key
        if team_id is not UNSET:
            field_dict["teamId"] = team_id
        if thumbnail_url is not UNSET:
            field_dict["thumbnailUrl"] = thumbnail_url
        if tlink is not UNSET:
            field_dict["tlink"] = tlink

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alt_page_url = d.pop("altPageUrl", UNSET)

        description = d.pop("description", UNSET)

        display_if_past = d.pop("displayIfPast", UNSET)

        distribution = d.pop("distribution", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        name = d.pop("name", UNSET)

        offer_id = d.pop("offerId", UNSET)

        offer_type = d.pop("offerType", UNSET)

        order = d.pop("order", UNSET)

        other = d.pop("other", UNSET)

        presented_by = d.pop("presentedBy", UNSET)

        sort_key = d.pop("sortKey", UNSET)

        team_id = d.pop("teamId", UNSET)

        thumbnail_url = d.pop("thumbnailUrl", UNSET)

        tlink = d.pop("tlink", UNSET)

        promotion_rest_object = cls(
            alt_page_url=alt_page_url,
            description=description,
            display_if_past=display_if_past,
            distribution=distribution,
            image_url=image_url,
            name=name,
            offer_id=offer_id,
            offer_type=offer_type,
            order=order,
            other=other,
            presented_by=presented_by,
            sort_key=sort_key,
            team_id=team_id,
            thumbnail_url=thumbnail_url,
            tlink=tlink,
        )

        promotion_rest_object.additional_properties = d
        return promotion_rest_object

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
