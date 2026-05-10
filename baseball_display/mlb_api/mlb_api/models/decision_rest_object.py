from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject


T = TypeVar("T", bound="DecisionRestObject")


@_attrs_define
class DecisionRestObject:
    """
    Attributes:
        loser (PersonRestObject | Unset):
        winner (PersonRestObject | Unset):
    """

    loser: PersonRestObject | Unset = UNSET
    winner: PersonRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject

        loser: dict[str, Any] | Unset = UNSET
        if not isinstance(self.loser, Unset):
            loser = self.loser.to_dict()

        winner: dict[str, Any] | Unset = UNSET
        if not isinstance(self.winner, Unset):
            winner = self.winner.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if loser is not UNSET:
            field_dict["loser"] = loser
        if winner is not UNSET:
            field_dict["winner"] = winner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject

        d = dict(src_dict)
        _loser = d.pop("loser", UNSET)
        loser: PersonRestObject | Unset
        if isinstance(_loser, Unset):
            loser = UNSET
        else:
            loser = PersonRestObject.from_dict(_loser)

        _winner = d.pop("winner", UNSET)
        winner: PersonRestObject | Unset
        if isinstance(_winner, Unset):
            winner = UNSET
        else:
            winner = PersonRestObject.from_dict(_winner)

        decision_rest_object = cls(
            loser=loser,
            winner=winner,
        )

        decision_rest_object.additional_properties = d
        return decision_rest_object

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
