from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.baseball_hit_data_rest_object import BaseballHitDataRestObject
    from ..models.home_run_derby_batter_hit_rest_object import (
        HomeRunDerbyBatterHitRestObject,
    )
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="HomeRunDerbyRoundBatterRestObject")


@_attrs_define
class HomeRunDerbyRoundBatterRestObject:
    """
    Attributes:
        hits (list[HomeRunDerbyBatterHitRestObject] | Unset):
        is_complete (bool | Unset):
        is_started (bool | Unset):
        is_winner (bool | Unset):
        num_home_runs (int | Unset):
        player (PersonRestObject | Unset):
        seed (int | Unset):
        top_derby_hit_data (BaseballHitDataRestObject | Unset):
    """

    hits: list[HomeRunDerbyBatterHitRestObject] | Unset = UNSET
    is_complete: bool | Unset = UNSET
    is_started: bool | Unset = UNSET
    is_winner: bool | Unset = UNSET
    num_home_runs: int | Unset = UNSET
    player: PersonRestObject | Unset = UNSET
    seed: int | Unset = UNSET
    top_derby_hit_data: BaseballHitDataRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.baseball_hit_data_rest_object import BaseballHitDataRestObject
        from ..models.home_run_derby_batter_hit_rest_object import (
            HomeRunDerbyBatterHitRestObject,
        )
        from ..models.person_rest_object import PersonRestObject

        hits: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.hits, Unset):
            hits = []
            for hits_item_data in self.hits:
                hits_item = hits_item_data.to_dict()
                hits.append(hits_item)

        is_complete = self.is_complete

        is_started = self.is_started

        is_winner = self.is_winner

        num_home_runs = self.num_home_runs

        player: dict[str, Any] | Unset = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        seed = self.seed

        top_derby_hit_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.top_derby_hit_data, Unset):
            top_derby_hit_data = self.top_derby_hit_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hits is not UNSET:
            field_dict["hits"] = hits
        if is_complete is not UNSET:
            field_dict["isComplete"] = is_complete
        if is_started is not UNSET:
            field_dict["isStarted"] = is_started
        if is_winner is not UNSET:
            field_dict["isWinner"] = is_winner
        if num_home_runs is not UNSET:
            field_dict["numHomeRuns"] = num_home_runs
        if player is not UNSET:
            field_dict["player"] = player
        if seed is not UNSET:
            field_dict["seed"] = seed
        if top_derby_hit_data is not UNSET:
            field_dict["topDerbyHitData"] = top_derby_hit_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseball_hit_data_rest_object import BaseballHitDataRestObject
        from ..models.home_run_derby_batter_hit_rest_object import (
            HomeRunDerbyBatterHitRestObject,
        )
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        _hits = d.pop("hits", UNSET)
        hits: list[HomeRunDerbyBatterHitRestObject] | Unset = UNSET
        if _hits is not UNSET:
            hits = []
            for hits_item_data in _hits:
                hits_item = HomeRunDerbyBatterHitRestObject.from_dict(hits_item_data)

                hits.append(hits_item)

        is_complete = d.pop("isComplete", UNSET)

        is_started = d.pop("isStarted", UNSET)

        is_winner = d.pop("isWinner", UNSET)

        num_home_runs = d.pop("numHomeRuns", UNSET)

        _player = d.pop("player", UNSET)
        player: PersonRestObject | Unset
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = PersonRestObject.from_dict(_player)

        seed = d.pop("seed", UNSET)

        _top_derby_hit_data = d.pop("topDerbyHitData", UNSET)
        top_derby_hit_data: BaseballHitDataRestObject | Unset
        if isinstance(_top_derby_hit_data, Unset):
            top_derby_hit_data = UNSET
        else:
            top_derby_hit_data = BaseballHitDataRestObject.from_dict(
                _top_derby_hit_data
            )

        home_run_derby_round_batter_rest_object = cls(
            hits=hits,
            is_complete=is_complete,
            is_started=is_started,
            is_winner=is_winner,
            num_home_runs=num_home_runs,
            player=player,
            seed=seed,
            top_derby_hit_data=top_derby_hit_data,
        )

        home_run_derby_round_batter_rest_object.additional_properties = d
        return home_run_derby_round_batter_rest_object

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
