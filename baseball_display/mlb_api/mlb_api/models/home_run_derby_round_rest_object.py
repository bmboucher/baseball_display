from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.home_run_derby_matchup_rest_object import (
        HomeRunDerbyMatchupRestObject,
    )
    from ..models.home_run_derby_round_batter_rest_object import (
        HomeRunDerbyRoundBatterRestObject,
    )


T = TypeVar("T", bound="HomeRunDerbyRoundRestObject")


@_attrs_define
class HomeRunDerbyRoundRestObject:
    """
    Attributes:
        batters (list[HomeRunDerbyRoundBatterRestObject] | Unset):
        matchups (list[HomeRunDerbyMatchupRestObject] | Unset):
        num_batters (int | Unset):
        round_ (int | Unset):
    """

    batters: list[HomeRunDerbyRoundBatterRestObject] | Unset = UNSET
    matchups: list[HomeRunDerbyMatchupRestObject] | Unset = UNSET
    num_batters: int | Unset = UNSET
    round_: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.home_run_derby_matchup_rest_object import (
            HomeRunDerbyMatchupRestObject,
        )
        from ..models.home_run_derby_round_batter_rest_object import (
            HomeRunDerbyRoundBatterRestObject,
        )

        batters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.batters, Unset):
            batters = []
            for batters_item_data in self.batters:
                batters_item = batters_item_data.to_dict()
                batters.append(batters_item)

        matchups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.matchups, Unset):
            matchups = []
            for matchups_item_data in self.matchups:
                matchups_item = matchups_item_data.to_dict()
                matchups.append(matchups_item)

        num_batters = self.num_batters

        round_ = self.round_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batters is not UNSET:
            field_dict["batters"] = batters
        if matchups is not UNSET:
            field_dict["matchups"] = matchups
        if num_batters is not UNSET:
            field_dict["numBatters"] = num_batters
        if round_ is not UNSET:
            field_dict["round"] = round_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.home_run_derby_matchup_rest_object import (
            HomeRunDerbyMatchupRestObject,
        )
        from ..models.home_run_derby_round_batter_rest_object import (
            HomeRunDerbyRoundBatterRestObject,
        )

        d = dict(src_dict)
        _batters = d.pop("batters", UNSET)
        batters: list[HomeRunDerbyRoundBatterRestObject] | Unset = UNSET
        if _batters is not UNSET:
            batters = []
            for batters_item_data in _batters:
                batters_item = HomeRunDerbyRoundBatterRestObject.from_dict(
                    batters_item_data
                )

                batters.append(batters_item)

        _matchups = d.pop("matchups", UNSET)
        matchups: list[HomeRunDerbyMatchupRestObject] | Unset = UNSET
        if _matchups is not UNSET:
            matchups = []
            for matchups_item_data in _matchups:
                matchups_item = HomeRunDerbyMatchupRestObject.from_dict(
                    matchups_item_data
                )

                matchups.append(matchups_item)

        num_batters = d.pop("numBatters", UNSET)

        round_ = d.pop("round", UNSET)

        home_run_derby_round_rest_object = cls(
            batters=batters,
            matchups=matchups,
            num_batters=num_batters,
            round_=round_,
        )

        home_run_derby_round_rest_object.additional_properties = d
        return home_run_derby_round_rest_object

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
