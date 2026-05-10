from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TicketRestObject")


@_attrs_define
class TicketRestObject:
    """
    Attributes:
        ticket_link (str | Unset):
        ticket_type (str | Unset):
    """

    ticket_link: str | Unset = UNSET
    ticket_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket_link = self.ticket_link

        ticket_type = self.ticket_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ticket_link is not UNSET:
            field_dict["ticketLink"] = ticket_link
        if ticket_type is not UNSET:
            field_dict["ticketType"] = ticket_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket_link = d.pop("ticketLink", UNSET)

        ticket_type = d.pop("ticketType", UNSET)

        ticket_rest_object = cls(
            ticket_link=ticket_link,
            ticket_type=ticket_type,
        )

        ticket_rest_object.additional_properties = d
        return ticket_rest_object

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
