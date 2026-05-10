from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameEditorialRestObject")


@_attrs_define
class GameEditorialRestObject:
    """
    Attributes:
        articles (Any | Unset):
        preview (Any | Unset):
        probables (Any | Unset):
        recap (Any | Unset):
        wrap (Any | Unset):
    """

    articles: Any | Unset = UNSET
    preview: Any | Unset = UNSET
    probables: Any | Unset = UNSET
    recap: Any | Unset = UNSET
    wrap: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        articles = self.articles

        preview = self.preview

        probables = self.probables

        recap = self.recap

        wrap = self.wrap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if articles is not UNSET:
            field_dict["articles"] = articles
        if preview is not UNSET:
            field_dict["preview"] = preview
        if probables is not UNSET:
            field_dict["probables"] = probables
        if recap is not UNSET:
            field_dict["recap"] = recap
        if wrap is not UNSET:
            field_dict["wrap"] = wrap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        articles = d.pop("articles", UNSET)

        preview = d.pop("preview", UNSET)

        probables = d.pop("probables", UNSET)

        recap = d.pop("recap", UNSET)

        wrap = d.pop("wrap", UNSET)

        game_editorial_rest_object = cls(
            articles=articles,
            preview=preview,
            probables=probables,
            recap=recap,
            wrap=wrap,
        )

        game_editorial_rest_object.additional_properties = d
        return game_editorial_rest_object

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
