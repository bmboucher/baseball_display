from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conference_rest_object import ConferenceRestObject
    from ..models.league_rest_object import LeagueRestObject
    from ..models.sport_rest_object import SportRestObject


T = TypeVar("T", bound="DivisionRestObject")


@_attrs_define
class DivisionRestObject:
    """
    Attributes:
        abbreviation (str | Unset): Shortened version of short name. Format: ALE, SFG
        conference (ConferenceRestObject | Unset):
        has_wildcard (bool | Unset): Whether or not there is a wildcard
        id (int | Unset): Unique Identifier
        league (LeagueRestObject | Unset):
        link (str | Unset): Link to full resource
        name (str | Unset): Unique Name
        name_short (str | Unset): Shortened version of name. Format: AL East, SF Giants
        sport (SportRestObject | Unset):
    """

    abbreviation: str | Unset = UNSET
    conference: ConferenceRestObject | Unset = UNSET
    has_wildcard: bool | Unset = UNSET
    id: int | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    link: str | Unset = UNSET
    name: str | Unset = UNSET
    name_short: str | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject

        abbreviation = self.abbreviation

        conference: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conference, Unset):
            conference = self.conference.to_dict()

        has_wildcard = self.has_wildcard

        id = self.id

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        link = self.link

        name = self.name

        name_short = self.name_short

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if conference is not UNSET:
            field_dict["conference"] = conference
        if has_wildcard is not UNSET:
            field_dict["hasWildcard"] = has_wildcard
        if id is not UNSET:
            field_dict["id"] = id
        if league is not UNSET:
            field_dict["league"] = league
        if link is not UNSET:
            field_dict["link"] = link
        if name is not UNSET:
            field_dict["name"] = name
        if name_short is not UNSET:
            field_dict["nameShort"] = name_short
        if sport is not UNSET:
            field_dict["sport"] = sport

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject

        d = dict(src_dict)
        abbreviation = d.pop("abbreviation", UNSET)

        _conference = d.pop("conference", UNSET)
        conference: ConferenceRestObject | Unset
        if isinstance(_conference, Unset):
            conference = UNSET
        else:
            conference = ConferenceRestObject.from_dict(_conference)

        has_wildcard = d.pop("hasWildcard", UNSET)

        id = d.pop("id", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        link = d.pop("link", UNSET)

        name = d.pop("name", UNSET)

        name_short = d.pop("nameShort", UNSET)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        division_rest_object = cls(
            abbreviation=abbreviation,
            conference=conference,
            has_wildcard=has_wildcard,
            id=id,
            league=league,
            link=link,
            name=name,
            name_short=name_short,
            sport=sport,
        )

        division_rest_object.additional_properties = d
        return division_rest_object

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
