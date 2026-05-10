from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="SeriesStatusRestObject")


@_attrs_define
class SeriesStatusRestObject:
    """
    Attributes:
        description (str | Unset):
        game_number (int | Unset):
        is_over (bool | Unset):
        is_tied (bool | Unset):
        losing_team (TeamRestObject | Unset):
        losses (int | Unset):
        result (str | Unset):
        short_description (str | Unset):
        short_name (str | Unset):
        ties (int | Unset):
        total_games (int | Unset):
        winning_team (TeamRestObject | Unset):
        wins (int | Unset):
    """

    description: str | Unset = UNSET
    game_number: int | Unset = UNSET
    is_over: bool | Unset = UNSET
    is_tied: bool | Unset = UNSET
    losing_team: TeamRestObject | Unset = UNSET
    losses: int | Unset = UNSET
    result: str | Unset = UNSET
    short_description: str | Unset = UNSET
    short_name: str | Unset = UNSET
    ties: int | Unset = UNSET
    total_games: int | Unset = UNSET
    winning_team: TeamRestObject | Unset = UNSET
    wins: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.team_rest_object import TeamRestObject

        description = self.description

        game_number = self.game_number

        is_over = self.is_over

        is_tied = self.is_tied

        losing_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.losing_team, Unset):
            losing_team = self.losing_team.to_dict()

        losses = self.losses

        result = self.result

        short_description = self.short_description

        short_name = self.short_name

        ties = self.ties

        total_games = self.total_games

        winning_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.winning_team, Unset):
            winning_team = self.winning_team.to_dict()

        wins = self.wins

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if game_number is not UNSET:
            field_dict["gameNumber"] = game_number
        if is_over is not UNSET:
            field_dict["isOver"] = is_over
        if is_tied is not UNSET:
            field_dict["isTied"] = is_tied
        if losing_team is not UNSET:
            field_dict["losingTeam"] = losing_team
        if losses is not UNSET:
            field_dict["losses"] = losses
        if result is not UNSET:
            field_dict["result"] = result
        if short_description is not UNSET:
            field_dict["shortDescription"] = short_description
        if short_name is not UNSET:
            field_dict["shortName"] = short_name
        if ties is not UNSET:
            field_dict["ties"] = ties
        if total_games is not UNSET:
            field_dict["totalGames"] = total_games
        if winning_team is not UNSET:
            field_dict["winningTeam"] = winning_team
        if wins is not UNSET:
            field_dict["wins"] = wins

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        description = d.pop("description", UNSET)

        game_number = d.pop("gameNumber", UNSET)

        is_over = d.pop("isOver", UNSET)

        is_tied = d.pop("isTied", UNSET)

        _losing_team = d.pop("losingTeam", UNSET)
        losing_team: TeamRestObject | Unset
        if isinstance(_losing_team, Unset):
            losing_team = UNSET
        else:
            losing_team = TeamRestObject.from_dict(_losing_team)

        losses = d.pop("losses", UNSET)

        result = d.pop("result", UNSET)

        short_description = d.pop("shortDescription", UNSET)

        short_name = d.pop("shortName", UNSET)

        ties = d.pop("ties", UNSET)

        total_games = d.pop("totalGames", UNSET)

        _winning_team = d.pop("winningTeam", UNSET)
        winning_team: TeamRestObject | Unset
        if isinstance(_winning_team, Unset):
            winning_team = UNSET
        else:
            winning_team = TeamRestObject.from_dict(_winning_team)

        wins = d.pop("wins", UNSET)

        series_status_rest_object = cls(
            description=description,
            game_number=game_number,
            is_over=is_over,
            is_tied=is_tied,
            losing_team=losing_team,
            losses=losses,
            result=result,
            short_description=short_description,
            short_name=short_name,
            ties=ties,
            total_games=total_games,
            winning_team=winning_team,
            wins=wins,
        )

        series_status_rest_object.additional_properties = d
        return series_status_rest_object

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
