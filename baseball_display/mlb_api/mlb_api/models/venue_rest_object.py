from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_rest_object import LocationRestObject
    from ..models.time_zone_rest_object import TimeZoneRestObject


T = TypeVar("T", bound="VenueRestObject")


@_attrs_define
class VenueRestObject:
    """
    Attributes:
        city (str | Unset): City where the venue is located. Format: Cleveland
        id (int | Unset): Unique Identifier
        link (str | Unset): Link to full resource
        location (LocationRestObject | Unset):
        name (str | Unset): Unique Name
        time_zone (TimeZoneRestObject | Unset):
    """

    city: str | Unset = UNSET
    id: int | Unset = UNSET
    link: str | Unset = UNSET
    location: LocationRestObject | Unset = UNSET
    name: str | Unset = UNSET
    time_zone: TimeZoneRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.location_rest_object import LocationRestObject
        from ..models.time_zone_rest_object import TimeZoneRestObject

        city = self.city

        id = self.id

        link = self.link

        location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        name = self.name

        time_zone: dict[str, Any] | Unset = UNSET
        if not isinstance(self.time_zone, Unset):
            time_zone = self.time_zone.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if city is not UNSET:
            field_dict["city"] = city
        if id is not UNSET:
            field_dict["id"] = id
        if link is not UNSET:
            field_dict["link"] = link
        if location is not UNSET:
            field_dict["location"] = location
        if name is not UNSET:
            field_dict["name"] = name
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_rest_object import LocationRestObject
        from ..models.time_zone_rest_object import TimeZoneRestObject

        d = dict(src_dict)
        city = d.pop("city", UNSET)

        id = d.pop("id", UNSET)

        link = d.pop("link", UNSET)

        _location = d.pop("location", UNSET)
        location: LocationRestObject | Unset
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = LocationRestObject.from_dict(_location)

        name = d.pop("name", UNSET)

        _time_zone = d.pop("timeZone", UNSET)
        time_zone: TimeZoneRestObject | Unset
        if isinstance(_time_zone, Unset):
            time_zone = UNSET
        else:
            time_zone = TimeZoneRestObject.from_dict(_time_zone)

        venue_rest_object = cls(
            city=city,
            id=id,
            link=link,
            location=location,
            name=name,
            time_zone=time_zone,
        )

        venue_rest_object.additional_properties = d
        return venue_rest_object

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
