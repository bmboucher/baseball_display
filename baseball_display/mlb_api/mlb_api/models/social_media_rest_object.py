from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SocialMediaRestObject")


@_attrs_define
class SocialMediaRestObject:
    """
    Attributes:
        facebook (list[str] | Unset): The player's username and ID. Format: Username - georgekontos70, ID -
            242731055756840
        googleplus (list[str] | Unset):
        hashtags (list[str] | Unset):
        instagram (list[str] | Unset): The player's username. Format: joepanik, hunterpence, etc
        periscope (list[str] | Unset):
        pinterest (list[str] | Unset):
        snapchat (list[str] | Unset):
        tumblr (list[str] | Unset):
        twitter (list[str] | Unset): The player's handle. Format: @Bbelt9, @bcraw35, etc
        vine (list[str] | Unset):
        website (list[str] | Unset):
        youtube (list[str] | Unset):
    """

    facebook: list[str] | Unset = UNSET
    googleplus: list[str] | Unset = UNSET
    hashtags: list[str] | Unset = UNSET
    instagram: list[str] | Unset = UNSET
    periscope: list[str] | Unset = UNSET
    pinterest: list[str] | Unset = UNSET
    snapchat: list[str] | Unset = UNSET
    tumblr: list[str] | Unset = UNSET
    twitter: list[str] | Unset = UNSET
    vine: list[str] | Unset = UNSET
    website: list[str] | Unset = UNSET
    youtube: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        facebook: list[str] | Unset = UNSET
        if not isinstance(self.facebook, Unset):
            facebook = self.facebook

        googleplus: list[str] | Unset = UNSET
        if not isinstance(self.googleplus, Unset):
            googleplus = self.googleplus

        hashtags: list[str] | Unset = UNSET
        if not isinstance(self.hashtags, Unset):
            hashtags = self.hashtags

        instagram: list[str] | Unset = UNSET
        if not isinstance(self.instagram, Unset):
            instagram = self.instagram

        periscope: list[str] | Unset = UNSET
        if not isinstance(self.periscope, Unset):
            periscope = self.periscope

        pinterest: list[str] | Unset = UNSET
        if not isinstance(self.pinterest, Unset):
            pinterest = self.pinterest

        snapchat: list[str] | Unset = UNSET
        if not isinstance(self.snapchat, Unset):
            snapchat = self.snapchat

        tumblr: list[str] | Unset = UNSET
        if not isinstance(self.tumblr, Unset):
            tumblr = self.tumblr

        twitter: list[str] | Unset = UNSET
        if not isinstance(self.twitter, Unset):
            twitter = self.twitter

        vine: list[str] | Unset = UNSET
        if not isinstance(self.vine, Unset):
            vine = self.vine

        website: list[str] | Unset = UNSET
        if not isinstance(self.website, Unset):
            website = self.website

        youtube: list[str] | Unset = UNSET
        if not isinstance(self.youtube, Unset):
            youtube = self.youtube

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if facebook is not UNSET:
            field_dict["facebook"] = facebook
        if googleplus is not UNSET:
            field_dict["googleplus"] = googleplus
        if hashtags is not UNSET:
            field_dict["hashtags"] = hashtags
        if instagram is not UNSET:
            field_dict["instagram"] = instagram
        if periscope is not UNSET:
            field_dict["periscope"] = periscope
        if pinterest is not UNSET:
            field_dict["pinterest"] = pinterest
        if snapchat is not UNSET:
            field_dict["snapchat"] = snapchat
        if tumblr is not UNSET:
            field_dict["tumblr"] = tumblr
        if twitter is not UNSET:
            field_dict["twitter"] = twitter
        if vine is not UNSET:
            field_dict["vine"] = vine
        if website is not UNSET:
            field_dict["website"] = website
        if youtube is not UNSET:
            field_dict["youtube"] = youtube

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        facebook = cast(list[str], d.pop("facebook", UNSET))

        googleplus = cast(list[str], d.pop("googleplus", UNSET))

        hashtags = cast(list[str], d.pop("hashtags", UNSET))

        instagram = cast(list[str], d.pop("instagram", UNSET))

        periscope = cast(list[str], d.pop("periscope", UNSET))

        pinterest = cast(list[str], d.pop("pinterest", UNSET))

        snapchat = cast(list[str], d.pop("snapchat", UNSET))

        tumblr = cast(list[str], d.pop("tumblr", UNSET))

        twitter = cast(list[str], d.pop("twitter", UNSET))

        vine = cast(list[str], d.pop("vine", UNSET))

        website = cast(list[str], d.pop("website", UNSET))

        youtube = cast(list[str], d.pop("youtube", UNSET))

        social_media_rest_object = cls(
            facebook=facebook,
            googleplus=googleplus,
            hashtags=hashtags,
            instagram=instagram,
            periscope=periscope,
            pinterest=pinterest,
            snapchat=snapchat,
            tumblr=tumblr,
            twitter=twitter,
            vine=vine,
            website=website,
            youtube=youtube,
        )

        social_media_rest_object.additional_properties = d
        return social_media_rest_object

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
