from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="AwardWinnerRestObject")


@_attrs_define
class AwardWinnerRestObject:
    """
    Attributes:
        coach (PersonRestObject | Unset):
        player (PersonRestObject | Unset):
        rank (str | Unset):
        team (TeamRestObject | Unset):
    """

    coach: PersonRestObject | Unset = UNSET
    player: PersonRestObject | Unset = UNSET
    rank: str | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject
        from ..models.team_rest_object import TeamRestObject

        coach: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coach, Unset):
            coach = self.coach.to_dict()

        player: dict[str, Any] | Unset = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        rank = self.rank

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if coach is not UNSET:
            field_dict["coach"] = coach
        if player is not UNSET:
            field_dict["player"] = player
        if rank is not UNSET:
            field_dict["rank"] = rank
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        _coach = d.pop("coach", UNSET)
        coach: PersonRestObject | Unset
        if isinstance(_coach, Unset):
            coach = UNSET
        else:
            coach = PersonRestObject.from_dict(_coach)

        _player = d.pop("player", UNSET)
        player: PersonRestObject | Unset
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = PersonRestObject.from_dict(_player)

        rank = d.pop("rank", UNSET)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        award_winner_rest_object = cls(
            coach=coach,
            player=player,
            rank=rank,
            team=team,
        )

        award_winner_rest_object.additional_properties = d
        return award_winner_rest_object

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
