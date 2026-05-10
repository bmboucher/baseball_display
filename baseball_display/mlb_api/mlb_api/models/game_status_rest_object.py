from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameStatusRestObject")


@_attrs_define
class GameStatusRestObject:
    """
    Attributes:
        abstract_game_state (str | Unset): Format: Preview, Live or Final
        coded_game_state (str | Unset): Single digit/letter status. Format: I = In Progress, F = Final
        detailed_state (str | Unset): Description of game state. Format: Delayed: Rain
        start_time_tbd (bool | Unset): Whether or not the start time is TBD
        status_code (str | Unset): Expanded version of coded game state. Format: IR = In Progress and Rain Delay
    """

    abstract_game_state: str | Unset = UNSET
    coded_game_state: str | Unset = UNSET
    detailed_state: str | Unset = UNSET
    start_time_tbd: bool | Unset = UNSET
    status_code: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        abstract_game_state = self.abstract_game_state

        coded_game_state = self.coded_game_state

        detailed_state = self.detailed_state

        start_time_tbd = self.start_time_tbd

        status_code = self.status_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abstract_game_state is not UNSET:
            field_dict["abstractGameState"] = abstract_game_state
        if coded_game_state is not UNSET:
            field_dict["codedGameState"] = coded_game_state
        if detailed_state is not UNSET:
            field_dict["detailedState"] = detailed_state
        if start_time_tbd is not UNSET:
            field_dict["startTimeTBD"] = start_time_tbd
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        abstract_game_state = d.pop("abstractGameState", UNSET)

        coded_game_state = d.pop("codedGameState", UNSET)

        detailed_state = d.pop("detailedState", UNSET)

        start_time_tbd = d.pop("startTimeTBD", UNSET)

        status_code = d.pop("statusCode", UNSET)

        game_status_rest_object = cls(
            abstract_game_state=abstract_game_state,
            coded_game_state=coded_game_state,
            detailed_state=detailed_state,
            start_time_tbd=start_time_tbd,
            status_code=status_code,
        )

        game_status_rest_object.additional_properties = d
        return game_status_rest_object

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
