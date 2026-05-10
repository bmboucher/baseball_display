from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameHighlightsRestObject")


@_attrs_define
class GameHighlightsRestObject:
    """
    Attributes:
        game_center (Any | Unset):
        highlights (Any | Unset):
        live (Any | Unset):
        milestone (Any | Unset):
        scoreboard (Any | Unset):
        scoreboard_preview (Any | Unset):
    """

    game_center: Any | Unset = UNSET
    highlights: Any | Unset = UNSET
    live: Any | Unset = UNSET
    milestone: Any | Unset = UNSET
    scoreboard: Any | Unset = UNSET
    scoreboard_preview: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        game_center = self.game_center

        highlights = self.highlights

        live = self.live

        milestone = self.milestone

        scoreboard = self.scoreboard

        scoreboard_preview = self.scoreboard_preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if game_center is not UNSET:
            field_dict["gameCenter"] = game_center
        if highlights is not UNSET:
            field_dict["highlights"] = highlights
        if live is not UNSET:
            field_dict["live"] = live
        if milestone is not UNSET:
            field_dict["milestone"] = milestone
        if scoreboard is not UNSET:
            field_dict["scoreboard"] = scoreboard
        if scoreboard_preview is not UNSET:
            field_dict["scoreboardPreview"] = scoreboard_preview

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        game_center = d.pop("gameCenter", UNSET)

        highlights = d.pop("highlights", UNSET)

        live = d.pop("live", UNSET)

        milestone = d.pop("milestone", UNSET)

        scoreboard = d.pop("scoreboard", UNSET)

        scoreboard_preview = d.pop("scoreboardPreview", UNSET)

        game_highlights_rest_object = cls(
            game_center=game_center,
            highlights=highlights,
            live=live,
            milestone=milestone,
            scoreboard=scoreboard,
            scoreboard_preview=scoreboard_preview,
        )

        game_highlights_rest_object.additional_properties = d
        return game_highlights_rest_object

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
