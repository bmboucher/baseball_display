from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="PlayerDraftInfoRestObject")


@_attrs_define
class PlayerDraftInfoRestObject:
    """
    Attributes:
        pick_in_round (int | Unset):
        pick_overall (int | Unset):
        round_ (str | Unset):
        team (TeamRestObject | Unset):
        year (int | Unset):
    """

    pick_in_round: int | Unset = UNSET
    pick_overall: int | Unset = UNSET
    round_: str | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    year: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.team_rest_object import TeamRestObject

        pick_in_round = self.pick_in_round

        pick_overall = self.pick_overall

        round_ = self.round_

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        year = self.year

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pick_in_round is not UNSET:
            field_dict["pickInRound"] = pick_in_round
        if pick_overall is not UNSET:
            field_dict["pickOverall"] = pick_overall
        if round_ is not UNSET:
            field_dict["round"] = round_
        if team is not UNSET:
            field_dict["team"] = team
        if year is not UNSET:
            field_dict["year"] = year

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        pick_in_round = d.pop("pickInRound", UNSET)

        pick_overall = d.pop("pickOverall", UNSET)

        round_ = d.pop("round", UNSET)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        year = d.pop("year", UNSET)

        player_draft_info_rest_object = cls(
            pick_in_round=pick_in_round,
            pick_overall=pick_overall,
            round_=round_,
            team=team,
            year=year,
        )

        player_draft_info_rest_object.additional_properties = d
        return player_draft_info_rest_object

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
