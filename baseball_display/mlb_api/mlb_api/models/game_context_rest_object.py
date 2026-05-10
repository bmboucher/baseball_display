from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schedule_item_rest_object import ScheduleItemRestObject


T = TypeVar("T", bound="GameContextRestObject")


@_attrs_define
class GameContextRestObject:
    """
    Attributes:
        away_team_win_probability (float | Unset): Away team winning probability
        game (ScheduleItemRestObject | Unset):
        home_team_win_probability (float | Unset): Home team winning probability
    """

    away_team_win_probability: float | Unset = UNSET
    game: ScheduleItemRestObject | Unset = UNSET
    home_team_win_probability: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.schedule_item_rest_object import ScheduleItemRestObject

        away_team_win_probability = self.away_team_win_probability

        game: dict[str, Any] | Unset = UNSET
        if not isinstance(self.game, Unset):
            game = self.game.to_dict()

        home_team_win_probability = self.home_team_win_probability

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if away_team_win_probability is not UNSET:
            field_dict["awayTeamWinProbability"] = away_team_win_probability
        if game is not UNSET:
            field_dict["game"] = game
        if home_team_win_probability is not UNSET:
            field_dict["homeTeamWinProbability"] = home_team_win_probability

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schedule_item_rest_object import ScheduleItemRestObject

        d = dict(src_dict)
        away_team_win_probability = d.pop("awayTeamWinProbability", UNSET)

        _game = d.pop("game", UNSET)
        game: ScheduleItemRestObject | Unset
        if isinstance(_game, Unset):
            game = UNSET
        else:
            game = ScheduleItemRestObject.from_dict(_game)

        home_team_win_probability = d.pop("homeTeamWinProbability", UNSET)

        game_context_rest_object = cls(
            away_team_win_probability=away_team_win_probability,
            game=game,
            home_team_win_probability=home_team_win_probability,
        )

        game_context_rest_object.additional_properties = d
        return game_context_rest_object

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
