from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stat_splits_rest_object import StatSplitsRestObject


T = TypeVar("T", bound="StatContainerRestObject")


@_attrs_define
class StatContainerRestObject:
    """
    Attributes:
        player (Any | Unset):
        season (str | Unset):
        splits (list[StatSplitsRestObject] | Unset): All of the details of stat splits
        splits_tied_with_limit (list[StatSplitsRestObject] | Unset):
        splits_tied_with_offset (list[StatSplitsRestObject] | Unset):
        stats (Any | Unset):
        team (Any | Unset):
        total_splits (int | Unset):
    """

    player: Any | Unset = UNSET
    season: str | Unset = UNSET
    splits: list[StatSplitsRestObject] | Unset = UNSET
    splits_tied_with_limit: list[StatSplitsRestObject] | Unset = UNSET
    splits_tied_with_offset: list[StatSplitsRestObject] | Unset = UNSET
    stats: Any | Unset = UNSET
    team: Any | Unset = UNSET
    total_splits: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.stat_splits_rest_object import StatSplitsRestObject

        player = self.player

        season = self.season

        splits: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.splits, Unset):
            splits = []
            for splits_item_data in self.splits:
                splits_item = splits_item_data.to_dict()
                splits.append(splits_item)

        splits_tied_with_limit: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.splits_tied_with_limit, Unset):
            splits_tied_with_limit = []
            for splits_tied_with_limit_item_data in self.splits_tied_with_limit:
                splits_tied_with_limit_item = splits_tied_with_limit_item_data.to_dict()
                splits_tied_with_limit.append(splits_tied_with_limit_item)

        splits_tied_with_offset: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.splits_tied_with_offset, Unset):
            splits_tied_with_offset = []
            for splits_tied_with_offset_item_data in self.splits_tied_with_offset:
                splits_tied_with_offset_item = (
                    splits_tied_with_offset_item_data.to_dict()
                )
                splits_tied_with_offset.append(splits_tied_with_offset_item)

        stats = self.stats

        team = self.team

        total_splits = self.total_splits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if player is not UNSET:
            field_dict["player"] = player
        if season is not UNSET:
            field_dict["season"] = season
        if splits is not UNSET:
            field_dict["splits"] = splits
        if splits_tied_with_limit is not UNSET:
            field_dict["splitsTiedWithLimit"] = splits_tied_with_limit
        if splits_tied_with_offset is not UNSET:
            field_dict["splitsTiedWithOffset"] = splits_tied_with_offset
        if stats is not UNSET:
            field_dict["stats"] = stats
        if team is not UNSET:
            field_dict["team"] = team
        if total_splits is not UNSET:
            field_dict["totalSplits"] = total_splits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.stat_splits_rest_object import StatSplitsRestObject

        d = dict(src_dict)
        player = d.pop("player", UNSET)

        season = d.pop("season", UNSET)

        _splits = d.pop("splits", UNSET)
        splits: list[StatSplitsRestObject] | Unset = UNSET
        if _splits is not UNSET:
            splits = []
            for splits_item_data in _splits:
                splits_item = StatSplitsRestObject.from_dict(splits_item_data)

                splits.append(splits_item)

        _splits_tied_with_limit = d.pop("splitsTiedWithLimit", UNSET)
        splits_tied_with_limit: list[StatSplitsRestObject] | Unset = UNSET
        if _splits_tied_with_limit is not UNSET:
            splits_tied_with_limit = []
            for splits_tied_with_limit_item_data in _splits_tied_with_limit:
                splits_tied_with_limit_item = StatSplitsRestObject.from_dict(
                    splits_tied_with_limit_item_data
                )

                splits_tied_with_limit.append(splits_tied_with_limit_item)

        _splits_tied_with_offset = d.pop("splitsTiedWithOffset", UNSET)
        splits_tied_with_offset: list[StatSplitsRestObject] | Unset = UNSET
        if _splits_tied_with_offset is not UNSET:
            splits_tied_with_offset = []
            for splits_tied_with_offset_item_data in _splits_tied_with_offset:
                splits_tied_with_offset_item = StatSplitsRestObject.from_dict(
                    splits_tied_with_offset_item_data
                )

                splits_tied_with_offset.append(splits_tied_with_offset_item)

        stats = d.pop("stats", UNSET)

        team = d.pop("team", UNSET)

        total_splits = d.pop("totalSplits", UNSET)

        stat_container_rest_object = cls(
            player=player,
            season=season,
            splits=splits,
            splits_tied_with_limit=splits_tied_with_limit,
            splits_tied_with_offset=splits_tied_with_offset,
            stats=stats,
            team=team,
            total_splits=total_splits,
        )

        stat_container_rest_object.additional_properties = d
        return stat_container_rest_object

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
