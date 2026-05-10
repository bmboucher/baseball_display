from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.home_run_derby_round_rest_object import HomeRunDerbyRoundRestObject
    from ..models.home_run_derby_status_rest_object import HomeRunDerbyStatusRestObject
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="HomeRunDerbyRestObject")


@_attrs_define
class HomeRunDerbyRestObject:
    """
    Attributes:
        info (Any | Unset):
        players (list[PersonRestObject] | Unset):
        rounds (list[HomeRunDerbyRoundRestObject] | Unset):
        status (HomeRunDerbyStatusRestObject | Unset):
    """

    info: Any | Unset = UNSET
    players: list[PersonRestObject] | Unset = UNSET
    rounds: list[HomeRunDerbyRoundRestObject] | Unset = UNSET
    status: HomeRunDerbyStatusRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.home_run_derby_round_rest_object import (
            HomeRunDerbyRoundRestObject,
        )
        from ..models.home_run_derby_status_rest_object import (
            HomeRunDerbyStatusRestObject,
        )
        from ..models.person_rest_object import PersonRestObject

        info = self.info

        players: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.players, Unset):
            players = []
            for players_item_data in self.players:
                players_item = players_item_data.to_dict()
                players.append(players_item)

        rounds: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rounds, Unset):
            rounds = []
            for rounds_item_data in self.rounds:
                rounds_item = rounds_item_data.to_dict()
                rounds.append(rounds_item)

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if info is not UNSET:
            field_dict["info"] = info
        if players is not UNSET:
            field_dict["players"] = players
        if rounds is not UNSET:
            field_dict["rounds"] = rounds
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.home_run_derby_round_rest_object import (
            HomeRunDerbyRoundRestObject,
        )
        from ..models.home_run_derby_status_rest_object import (
            HomeRunDerbyStatusRestObject,
        )
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        info = d.pop("info", UNSET)

        _players = d.pop("players", UNSET)
        players: list[PersonRestObject] | Unset = UNSET
        if _players is not UNSET:
            players = []
            for players_item_data in _players:
                players_item = PersonRestObject.from_dict(players_item_data)

                players.append(players_item)

        _rounds = d.pop("rounds", UNSET)
        rounds: list[HomeRunDerbyRoundRestObject] | Unset = UNSET
        if _rounds is not UNSET:
            rounds = []
            for rounds_item_data in _rounds:
                rounds_item = HomeRunDerbyRoundRestObject.from_dict(rounds_item_data)

                rounds.append(rounds_item)

        _status = d.pop("status", UNSET)
        status: HomeRunDerbyStatusRestObject | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = HomeRunDerbyStatusRestObject.from_dict(_status)

        home_run_derby_rest_object = cls(
            info=info,
            players=players,
            rounds=rounds,
            status=status,
        )

        home_run_derby_rest_object.additional_properties = d
        return home_run_derby_rest_object

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
