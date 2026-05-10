from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameContentSummaryRestObject")


@_attrs_define
class GameContentSummaryRestObject:
    """
    Attributes:
        has_highlights_video (bool | Unset):
        has_preview_article (bool | Unset):
        has_recap_article (bool | Unset):
        has_wrap_article (bool | Unset):
    """

    has_highlights_video: bool | Unset = UNSET
    has_preview_article: bool | Unset = UNSET
    has_recap_article: bool | Unset = UNSET
    has_wrap_article: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_highlights_video = self.has_highlights_video

        has_preview_article = self.has_preview_article

        has_recap_article = self.has_recap_article

        has_wrap_article = self.has_wrap_article

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if has_highlights_video is not UNSET:
            field_dict["hasHighlightsVideo"] = has_highlights_video
        if has_preview_article is not UNSET:
            field_dict["hasPreviewArticle"] = has_preview_article
        if has_recap_article is not UNSET:
            field_dict["hasRecapArticle"] = has_recap_article
        if has_wrap_article is not UNSET:
            field_dict["hasWrapArticle"] = has_wrap_article

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_highlights_video = d.pop("hasHighlightsVideo", UNSET)

        has_preview_article = d.pop("hasPreviewArticle", UNSET)

        has_recap_article = d.pop("hasRecapArticle", UNSET)

        has_wrap_article = d.pop("hasWrapArticle", UNSET)

        game_content_summary_rest_object = cls(
            has_highlights_video=has_highlights_video,
            has_preview_article=has_preview_article,
            has_recap_article=has_recap_article,
            has_wrap_article=has_wrap_article,
        )

        game_content_summary_rest_object.additional_properties = d
        return game_content_summary_rest_object

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
