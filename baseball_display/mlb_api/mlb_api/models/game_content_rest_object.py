from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.game_content_summary_rest_object import GameContentSummaryRestObject
    from ..models.game_editorial_rest_object import GameEditorialRestObject
    from ..models.game_highlights_rest_object import GameHighlightsRestObject
    from ..models.game_media_rest_object import GameMediaRestObject
    from ..models.game_notes_rest_object import GameNotesRestObject


T = TypeVar("T", bound="GameContentRestObject")


@_attrs_define
class GameContentRestObject:
    """
    Attributes:
        editorial (GameEditorialRestObject | Unset):
        game_notes (GameNotesRestObject | Unset):
        highlights (GameHighlightsRestObject | Unset):
        link (str | Unset): Link to full resource
        media (GameMediaRestObject | Unset):
        summary (GameContentSummaryRestObject | Unset):
    """

    editorial: GameEditorialRestObject | Unset = UNSET
    game_notes: GameNotesRestObject | Unset = UNSET
    highlights: GameHighlightsRestObject | Unset = UNSET
    link: str | Unset = UNSET
    media: GameMediaRestObject | Unset = UNSET
    summary: GameContentSummaryRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.game_content_summary_rest_object import (
            GameContentSummaryRestObject,
        )
        from ..models.game_editorial_rest_object import GameEditorialRestObject
        from ..models.game_highlights_rest_object import GameHighlightsRestObject
        from ..models.game_media_rest_object import GameMediaRestObject
        from ..models.game_notes_rest_object import GameNotesRestObject

        editorial: dict[str, Any] | Unset = UNSET
        if not isinstance(self.editorial, Unset):
            editorial = self.editorial.to_dict()

        game_notes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.game_notes, Unset):
            game_notes = self.game_notes.to_dict()

        highlights: dict[str, Any] | Unset = UNSET
        if not isinstance(self.highlights, Unset):
            highlights = self.highlights.to_dict()

        link = self.link

        media: dict[str, Any] | Unset = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.to_dict()

        summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if editorial is not UNSET:
            field_dict["editorial"] = editorial
        if game_notes is not UNSET:
            field_dict["gameNotes"] = game_notes
        if highlights is not UNSET:
            field_dict["highlights"] = highlights
        if link is not UNSET:
            field_dict["link"] = link
        if media is not UNSET:
            field_dict["media"] = media
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.game_content_summary_rest_object import (
            GameContentSummaryRestObject,
        )
        from ..models.game_editorial_rest_object import GameEditorialRestObject
        from ..models.game_highlights_rest_object import GameHighlightsRestObject
        from ..models.game_media_rest_object import GameMediaRestObject
        from ..models.game_notes_rest_object import GameNotesRestObject

        d = dict(src_dict)
        _editorial = d.pop("editorial", UNSET)
        editorial: GameEditorialRestObject | Unset
        if isinstance(_editorial, Unset):
            editorial = UNSET
        else:
            editorial = GameEditorialRestObject.from_dict(_editorial)

        _game_notes = d.pop("gameNotes", UNSET)
        game_notes: GameNotesRestObject | Unset
        if isinstance(_game_notes, Unset):
            game_notes = UNSET
        else:
            game_notes = GameNotesRestObject.from_dict(_game_notes)

        _highlights = d.pop("highlights", UNSET)
        highlights: GameHighlightsRestObject | Unset
        if isinstance(_highlights, Unset):
            highlights = UNSET
        else:
            highlights = GameHighlightsRestObject.from_dict(_highlights)

        link = d.pop("link", UNSET)

        _media = d.pop("media", UNSET)
        media: GameMediaRestObject | Unset
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = GameMediaRestObject.from_dict(_media)

        _summary = d.pop("summary", UNSET)
        summary: GameContentSummaryRestObject | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = GameContentSummaryRestObject.from_dict(_summary)

        game_content_rest_object = cls(
            editorial=editorial,
            game_notes=game_notes,
            highlights=highlights,
            link=link,
            media=media,
            summary=summary,
        )

        game_content_rest_object.additional_properties = d
        return game_content_rest_object

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
