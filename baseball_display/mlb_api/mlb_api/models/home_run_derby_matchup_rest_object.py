from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.home_run_derby_round_batter_rest_object import (
        HomeRunDerbyRoundBatterRestObject,
    )


T = TypeVar("T", bound="HomeRunDerbyMatchupRestObject")


@_attrs_define
class HomeRunDerbyMatchupRestObject:
    """
    Attributes:
        bottom_seed (HomeRunDerbyRoundBatterRestObject | Unset):
        top_seed (HomeRunDerbyRoundBatterRestObject | Unset):
    """

    bottom_seed: HomeRunDerbyRoundBatterRestObject | Unset = UNSET
    top_seed: HomeRunDerbyRoundBatterRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.home_run_derby_round_batter_rest_object import (
            HomeRunDerbyRoundBatterRestObject,
        )

        bottom_seed: dict[str, Any] | Unset = UNSET
        if not isinstance(self.bottom_seed, Unset):
            bottom_seed = self.bottom_seed.to_dict()

        top_seed: dict[str, Any] | Unset = UNSET
        if not isinstance(self.top_seed, Unset):
            top_seed = self.top_seed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bottom_seed is not UNSET:
            field_dict["bottomSeed"] = bottom_seed
        if top_seed is not UNSET:
            field_dict["topSeed"] = top_seed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.home_run_derby_round_batter_rest_object import (
            HomeRunDerbyRoundBatterRestObject,
        )

        d = dict(src_dict)
        _bottom_seed = d.pop("bottomSeed", UNSET)
        bottom_seed: HomeRunDerbyRoundBatterRestObject | Unset
        if isinstance(_bottom_seed, Unset):
            bottom_seed = UNSET
        else:
            bottom_seed = HomeRunDerbyRoundBatterRestObject.from_dict(_bottom_seed)

        _top_seed = d.pop("topSeed", UNSET)
        top_seed: HomeRunDerbyRoundBatterRestObject | Unset
        if isinstance(_top_seed, Unset):
            top_seed = UNSET
        else:
            top_seed = HomeRunDerbyRoundBatterRestObject.from_dict(_top_seed)

        home_run_derby_matchup_rest_object = cls(
            bottom_seed=bottom_seed,
            top_seed=top_seed,
        )

        home_run_derby_matchup_rest_object.additional_properties = d
        return home_run_derby_matchup_rest_object

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
