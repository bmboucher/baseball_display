from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SituationCodeRestObject")


@_attrs_define
class SituationCodeRestObject:
    """
    Attributes:
        batting (bool | Unset):
        code (str | Unset):
        description (str | Unset):
        fielding (bool | Unset):
        navigation_menu (str | Unset):
        pitching (bool | Unset):
        sort_order (int | Unset):
        team (bool | Unset):
    """

    batting: bool | Unset = UNSET
    code: str | Unset = UNSET
    description: str | Unset = UNSET
    fielding: bool | Unset = UNSET
    navigation_menu: str | Unset = UNSET
    pitching: bool | Unset = UNSET
    sort_order: int | Unset = UNSET
    team: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        batting = self.batting

        code = self.code

        description = self.description

        fielding = self.fielding

        navigation_menu = self.navigation_menu

        pitching = self.pitching

        sort_order = self.sort_order

        team = self.team

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batting is not UNSET:
            field_dict["batting"] = batting
        if code is not UNSET:
            field_dict["code"] = code
        if description is not UNSET:
            field_dict["description"] = description
        if fielding is not UNSET:
            field_dict["fielding"] = fielding
        if navigation_menu is not UNSET:
            field_dict["navigationMenu"] = navigation_menu
        if pitching is not UNSET:
            field_dict["pitching"] = pitching
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batting = d.pop("batting", UNSET)

        code = d.pop("code", UNSET)

        description = d.pop("description", UNSET)

        fielding = d.pop("fielding", UNSET)

        navigation_menu = d.pop("navigationMenu", UNSET)

        pitching = d.pop("pitching", UNSET)

        sort_order = d.pop("sortOrder", UNSET)

        team = d.pop("team", UNSET)

        situation_code_rest_object = cls(
            batting=batting,
            code=code,
            description=description,
            fielding=fielding,
            navigation_menu=navigation_menu,
            pitching=pitching,
            sort_order=sort_order,
            team=team,
        )

        situation_code_rest_object.additional_properties = d
        return situation_code_rest_object

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
