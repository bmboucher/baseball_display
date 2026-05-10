from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_rest_object import DecisionRestObject
    from ..models.play_by_play_rest_object import PlayByPlayRestObject


T = TypeVar("T", bound="GameLiveDataRestObject")


@_attrs_define
class GameLiveDataRestObject:
    """
    Attributes:
        decisions (DecisionRestObject | Unset):
        plays (PlayByPlayRestObject | Unset):
    """

    decisions: DecisionRestObject | Unset = UNSET
    plays: PlayByPlayRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.decision_rest_object import DecisionRestObject
        from ..models.play_by_play_rest_object import PlayByPlayRestObject

        decisions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decisions, Unset):
            decisions = self.decisions.to_dict()

        plays: dict[str, Any] | Unset = UNSET
        if not isinstance(self.plays, Unset):
            plays = self.plays.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if decisions is not UNSET:
            field_dict["decisions"] = decisions
        if plays is not UNSET:
            field_dict["plays"] = plays

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_rest_object import DecisionRestObject
        from ..models.play_by_play_rest_object import PlayByPlayRestObject

        d = dict(src_dict)
        _decisions = d.pop("decisions", UNSET)
        decisions: DecisionRestObject | Unset
        if isinstance(_decisions, Unset):
            decisions = UNSET
        else:
            decisions = DecisionRestObject.from_dict(_decisions)

        _plays = d.pop("plays", UNSET)
        plays: PlayByPlayRestObject | Unset
        if isinstance(_plays, Unset):
            plays = UNSET
        else:
            plays = PlayByPlayRestObject.from_dict(_plays)

        game_live_data_rest_object = cls(
            decisions=decisions,
            plays=plays,
        )

        game_live_data_rest_object.additional_properties = d
        return game_live_data_rest_object

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
