from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_rest_object import PersonRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="TransactionRestObject")


@_attrs_define
class TransactionRestObject:
    """
    Attributes:
        date (datetime.datetime | Unset):
        description (str | Unset):
        effective_date (datetime.datetime | Unset):
        from_team (TeamRestObject | Unset):
        id (int | Unset):
        is_conditional (bool | Unset):
        person (PersonRestObject | Unset):
        resolution_date (datetime.datetime | Unset):
        to_team (TeamRestObject | Unset):
        type_ (str | Unset):
    """

    date: datetime.datetime | Unset = UNSET
    description: str | Unset = UNSET
    effective_date: datetime.datetime | Unset = UNSET
    from_team: TeamRestObject | Unset = UNSET
    id: int | Unset = UNSET
    is_conditional: bool | Unset = UNSET
    person: PersonRestObject | Unset = UNSET
    resolution_date: datetime.datetime | Unset = UNSET
    to_team: TeamRestObject | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.person_rest_object import PersonRestObject
        from ..models.team_rest_object import TeamRestObject

        date: str | Unset = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        description = self.description

        effective_date: str | Unset = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        from_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.from_team, Unset):
            from_team = self.from_team.to_dict()

        id = self.id

        is_conditional = self.is_conditional

        person: dict[str, Any] | Unset = UNSET
        if not isinstance(self.person, Unset):
            person = self.person.to_dict()

        resolution_date: str | Unset = UNSET
        if not isinstance(self.resolution_date, Unset):
            resolution_date = self.resolution_date.isoformat()

        to_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.to_team, Unset):
            to_team = self.to_team.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if description is not UNSET:
            field_dict["description"] = description
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date
        if from_team is not UNSET:
            field_dict["fromTeam"] = from_team
        if id is not UNSET:
            field_dict["id"] = id
        if is_conditional is not UNSET:
            field_dict["isConditional"] = is_conditional
        if person is not UNSET:
            field_dict["person"] = person
        if resolution_date is not UNSET:
            field_dict["resolutionDate"] = resolution_date
        if to_team is not UNSET:
            field_dict["toTeam"] = to_team
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_rest_object import PersonRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        _date = d.pop("date", UNSET)
        date: datetime.datetime | Unset
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        description = d.pop("description", UNSET)

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: datetime.datetime | Unset
        if isinstance(_effective_date, Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date)

        _from_team = d.pop("fromTeam", UNSET)
        from_team: TeamRestObject | Unset
        if isinstance(_from_team, Unset):
            from_team = UNSET
        else:
            from_team = TeamRestObject.from_dict(_from_team)

        id = d.pop("id", UNSET)

        is_conditional = d.pop("isConditional", UNSET)

        _person = d.pop("person", UNSET)
        person: PersonRestObject | Unset
        if isinstance(_person, Unset):
            person = UNSET
        else:
            person = PersonRestObject.from_dict(_person)

        _resolution_date = d.pop("resolutionDate", UNSET)
        resolution_date: datetime.datetime | Unset
        if isinstance(_resolution_date, Unset):
            resolution_date = UNSET
        else:
            resolution_date = isoparse(_resolution_date)

        _to_team = d.pop("toTeam", UNSET)
        to_team: TeamRestObject | Unset
        if isinstance(_to_team, Unset):
            to_team = UNSET
        else:
            to_team = TeamRestObject.from_dict(_to_team)

        type_ = d.pop("type", UNSET)

        transaction_rest_object = cls(
            date=date,
            description=description,
            effective_date=effective_date,
            from_team=from_team,
            id=id,
            is_conditional=is_conditional,
            person=person,
            resolution_date=resolution_date,
            to_team=to_team,
            type_=type_,
        )

        transaction_rest_object.additional_properties = d
        return transaction_rest_object

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
