from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="HomeRunDerbyStatusRestObject")


@_attrs_define
class HomeRunDerbyStatusRestObject:
    """
    Attributes:
        bonus_time (bool | Unset):
        clock_stopped (bool | Unset):
        current_batter (PersonRestObject | Unset):
        current_round (int | Unset):
        current_round_in_progress (bool | Unset):
        current_round_time_left (str | Unset):
        in_tie_breaker (bool | Unset):
        scheduled_rounds (int | Unset):
        state (str | Unset):
        tie_breaker_num (int | Unset):
    """

    bonus_time: bool | Unset = UNSET
    clock_stopped: bool | Unset = UNSET
    current_batter: PersonRestObject | Unset = UNSET
    current_round: int | Unset = UNSET
    current_round_in_progress: bool | Unset = UNSET
    current_round_time_left: str | Unset = UNSET
    in_tie_breaker: bool | Unset = UNSET
    scheduled_rounds: int | Unset = UNSET
    state: str | Unset = UNSET
    tie_breaker_num: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject

        bonus_time = self.bonus_time

        clock_stopped = self.clock_stopped

        current_batter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.current_batter, Unset):
            current_batter = self.current_batter.to_dict()

        current_round = self.current_round

        current_round_in_progress = self.current_round_in_progress

        current_round_time_left = self.current_round_time_left

        in_tie_breaker = self.in_tie_breaker

        scheduled_rounds = self.scheduled_rounds

        state = self.state

        tie_breaker_num = self.tie_breaker_num

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bonus_time is not UNSET:
            field_dict["bonusTime"] = bonus_time
        if clock_stopped is not UNSET:
            field_dict["clockStopped"] = clock_stopped
        if current_batter is not UNSET:
            field_dict["currentBatter"] = current_batter
        if current_round is not UNSET:
            field_dict["currentRound"] = current_round
        if current_round_in_progress is not UNSET:
            field_dict["currentRoundInProgress"] = current_round_in_progress
        if current_round_time_left is not UNSET:
            field_dict["currentRoundTimeLeft"] = current_round_time_left
        if in_tie_breaker is not UNSET:
            field_dict["inTieBreaker"] = in_tie_breaker
        if scheduled_rounds is not UNSET:
            field_dict["scheduledRounds"] = scheduled_rounds
        if state is not UNSET:
            field_dict["state"] = state
        if tie_breaker_num is not UNSET:
            field_dict["tieBreakerNum"] = tie_breaker_num

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        bonus_time = d.pop("bonusTime", UNSET)

        clock_stopped = d.pop("clockStopped", UNSET)

        _current_batter = d.pop("currentBatter", UNSET)
        current_batter: PersonRestObject | Unset
        if isinstance(_current_batter, Unset):
            current_batter = UNSET
        else:
            current_batter = PersonRestObject.from_dict(_current_batter)

        current_round = d.pop("currentRound", UNSET)

        current_round_in_progress = d.pop("currentRoundInProgress", UNSET)

        current_round_time_left = d.pop("currentRoundTimeLeft", UNSET)

        in_tie_breaker = d.pop("inTieBreaker", UNSET)

        scheduled_rounds = d.pop("scheduledRounds", UNSET)

        state = d.pop("state", UNSET)

        tie_breaker_num = d.pop("tieBreakerNum", UNSET)

        home_run_derby_status_rest_object = cls(
            bonus_time=bonus_time,
            clock_stopped=clock_stopped,
            current_batter=current_batter,
            current_round=current_round,
            current_round_in_progress=current_round_in_progress,
            current_round_time_left=current_round_time_left,
            in_tie_breaker=in_tie_breaker,
            scheduled_rounds=scheduled_rounds,
            state=state,
            tie_breaker_num=tie_breaker_num,
        )

        home_run_derby_status_rest_object.additional_properties = d
        return home_run_derby_status_rest_object

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
