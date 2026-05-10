from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.baseball_person_rest_object import BaseballPersonRestObject
    from ..models.position_rest_object import PositionRestObject


T = TypeVar("T", bound="FreeAgentRestObject")


@_attrs_define
class FreeAgentRestObject:
    """
    Attributes:
        date_declared (datetime.datetime | Unset):
        date_signed (datetime.datetime | Unset):
        new_team (Any | Unset):
        notes (str | Unset):
        original_team (Any | Unset):
        player (BaseballPersonRestObject | Unset):
        position (PositionRestObject | Unset):
        sort_order (int | Unset):
        url (str | Unset):
    """

    date_declared: datetime.datetime | Unset = UNSET
    date_signed: datetime.datetime | Unset = UNSET
    new_team: Any | Unset = UNSET
    notes: str | Unset = UNSET
    original_team: Any | Unset = UNSET
    player: BaseballPersonRestObject | Unset = UNSET
    position: PositionRestObject | Unset = UNSET
    sort_order: int | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.baseball_person_rest_object import BaseballPersonRestObject
        from ..models.position_rest_object import PositionRestObject

        date_declared: str | Unset = UNSET
        if not isinstance(self.date_declared, Unset):
            date_declared = self.date_declared.isoformat()

        date_signed: str | Unset = UNSET
        if not isinstance(self.date_signed, Unset):
            date_signed = self.date_signed.isoformat()

        new_team = self.new_team

        notes = self.notes

        original_team = self.original_team

        player: dict[str, Any] | Unset = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        sort_order = self.sort_order

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date_declared is not UNSET:
            field_dict["dateDeclared"] = date_declared
        if date_signed is not UNSET:
            field_dict["dateSigned"] = date_signed
        if new_team is not UNSET:
            field_dict["newTeam"] = new_team
        if notes is not UNSET:
            field_dict["notes"] = notes
        if original_team is not UNSET:
            field_dict["originalTeam"] = original_team
        if player is not UNSET:
            field_dict["player"] = player
        if position is not UNSET:
            field_dict["position"] = position
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseball_person_rest_object import BaseballPersonRestObject
        from ..models.position_rest_object import PositionRestObject

        d = dict(src_dict)
        _date_declared = d.pop("dateDeclared", UNSET)
        date_declared: datetime.datetime | Unset
        if isinstance(_date_declared, Unset):
            date_declared = UNSET
        else:
            date_declared = isoparse(_date_declared)

        _date_signed = d.pop("dateSigned", UNSET)
        date_signed: datetime.datetime | Unset
        if isinstance(_date_signed, Unset):
            date_signed = UNSET
        else:
            date_signed = isoparse(_date_signed)

        new_team = d.pop("newTeam", UNSET)

        notes = d.pop("notes", UNSET)

        original_team = d.pop("originalTeam", UNSET)

        _player = d.pop("player", UNSET)
        player: BaseballPersonRestObject | Unset
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = BaseballPersonRestObject.from_dict(_player)

        _position = d.pop("position", UNSET)
        position: PositionRestObject | Unset
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = PositionRestObject.from_dict(_position)

        sort_order = d.pop("sortOrder", UNSET)

        url = d.pop("url", UNSET)

        free_agent_rest_object = cls(
            date_declared=date_declared,
            date_signed=date_signed,
            new_team=new_team,
            notes=notes,
            original_team=original_team,
            player=player,
            position=position,
            sort_order=sort_order,
            url=url,
        )

        free_agent_rest_object.additional_properties = d
        return free_agent_rest_object

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
