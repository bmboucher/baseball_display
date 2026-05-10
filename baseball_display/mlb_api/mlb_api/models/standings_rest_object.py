from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_standings_record_container_rest_object import (
        TeamStandingsRecordContainerRestObject,
    )


T = TypeVar("T", bound="StandingsRestObject")


@_attrs_define
class StandingsRestObject:
    """
    Attributes:
        last_updated (datetime.datetime | Unset):
        records (list[TeamStandingsRecordContainerRestObject] | Unset):
    """

    last_updated: datetime.datetime | Unset = UNSET
    records: list[TeamStandingsRecordContainerRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.team_standings_record_container_rest_object import (
            TeamStandingsRecordContainerRestObject,
        )

        last_updated: str | Unset = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item = records_item_data.to_dict()
                records.append(records_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if last_updated is not UNSET:
            field_dict["lastUpdated"] = last_updated
        if records is not UNSET:
            field_dict["records"] = records

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.team_standings_record_container_rest_object import (
            TeamStandingsRecordContainerRestObject,
        )

        d = dict(src_dict)
        _last_updated = d.pop("lastUpdated", UNSET)
        last_updated: datetime.datetime | Unset
        if isinstance(_last_updated, Unset):
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        _records = d.pop("records", UNSET)
        records: list[TeamStandingsRecordContainerRestObject] | Unset = UNSET
        if _records is not UNSET:
            records = []
            for records_item_data in _records:
                records_item = TeamStandingsRecordContainerRestObject.from_dict(
                    records_item_data
                )

                records.append(records_item)

        standings_rest_object = cls(
            last_updated=last_updated,
            records=records,
        )

        standings_rest_object.additional_properties = d
        return standings_rest_object

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
