from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameMediaRestObject")


@_attrs_define
class GameMediaRestObject:
    """
    Attributes:
        enhanced_game (bool | Unset): Whether or not the game is enhanced
        epg (Any | Unset):
        epg_alternate (Any | Unset):
        featured_media (Any | Unset):
        free_game (bool | Unset): Whether or not the game is free
        milestones (Any | Unset):
    """

    enhanced_game: bool | Unset = UNSET
    epg: Any | Unset = UNSET
    epg_alternate: Any | Unset = UNSET
    featured_media: Any | Unset = UNSET
    free_game: bool | Unset = UNSET
    milestones: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enhanced_game = self.enhanced_game

        epg = self.epg

        epg_alternate = self.epg_alternate

        featured_media = self.featured_media

        free_game = self.free_game

        milestones = self.milestones

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enhanced_game is not UNSET:
            field_dict["enhancedGame"] = enhanced_game
        if epg is not UNSET:
            field_dict["epg"] = epg
        if epg_alternate is not UNSET:
            field_dict["epgAlternate"] = epg_alternate
        if featured_media is not UNSET:
            field_dict["featuredMedia"] = featured_media
        if free_game is not UNSET:
            field_dict["freeGame"] = free_game
        if milestones is not UNSET:
            field_dict["milestones"] = milestones

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enhanced_game = d.pop("enhancedGame", UNSET)

        epg = d.pop("epg", UNSET)

        epg_alternate = d.pop("epgAlternate", UNSET)

        featured_media = d.pop("featuredMedia", UNSET)

        free_game = d.pop("freeGame", UNSET)

        milestones = d.pop("milestones", UNSET)

        game_media_rest_object = cls(
            enhanced_game=enhanced_game,
            epg=epg,
            epg_alternate=epg_alternate,
            featured_media=featured_media,
            free_game=free_game,
            milestones=milestones,
        )

        game_media_rest_object.additional_properties = d
        return game_media_rest_object

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
