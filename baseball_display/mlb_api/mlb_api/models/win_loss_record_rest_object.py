from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WinLossRecordRestObject")


@_attrs_define
class WinLossRecordRestObject:
    """
    Attributes:
        losses (int | Unset):
        pct (str | Unset):
        ties (int | Unset):
        type_ (str | Unset):
        wins (int | Unset):
    """

    losses: int | Unset = UNSET
    pct: str | Unset = UNSET
    ties: int | Unset = UNSET
    type_: str | Unset = UNSET
    wins: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        losses = self.losses

        pct = self.pct

        ties = self.ties

        type_ = self.type_

        wins = self.wins

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if losses is not UNSET:
            field_dict["losses"] = losses
        if pct is not UNSET:
            field_dict["pct"] = pct
        if ties is not UNSET:
            field_dict["ties"] = ties
        if type_ is not UNSET:
            field_dict["type"] = type_
        if wins is not UNSET:
            field_dict["wins"] = wins

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        losses = d.pop("losses", UNSET)

        pct = d.pop("pct", UNSET)

        ties = d.pop("ties", UNSET)

        type_ = d.pop("type", UNSET)

        wins = d.pop("wins", UNSET)

        win_loss_record_rest_object = cls(
            losses=losses,
            pct=pct,
            ties=ties,
            type_=type_,
            wins=wins,
        )

        win_loss_record_rest_object.additional_properties = d
        return win_loss_record_rest_object

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
