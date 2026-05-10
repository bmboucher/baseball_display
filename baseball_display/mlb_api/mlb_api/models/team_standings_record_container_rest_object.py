from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conference_rest_object import ConferenceRestObject
    from ..models.division_rest_object import DivisionRestObject
    from ..models.league_rest_object import LeagueRestObject
    from ..models.sport_rest_object import SportRestObject
    from ..models.team_rest_object import TeamRestObject
    from ..models.team_standings_record_rest_object import TeamStandingsRecordRestObject


T = TypeVar("T", bound="TeamStandingsRecordContainerRestObject")


@_attrs_define
class TeamStandingsRecordContainerRestObject:
    """
    Attributes:
        aggregate_record (TeamStandingsRecordRestObject | Unset):
        conference (ConferenceRestObject | Unset):
        division (DivisionRestObject | Unset):
        last_updated (datetime.datetime | Unset):
        league (LeagueRestObject | Unset):
        organization (TeamRestObject | Unset):
        sport (SportRestObject | Unset):
        standings_type (str | Unset):
        team_records (list[TeamStandingsRecordRestObject] | Unset):
    """

    aggregate_record: TeamStandingsRecordRestObject | Unset = UNSET
    conference: ConferenceRestObject | Unset = UNSET
    division: DivisionRestObject | Unset = UNSET
    last_updated: datetime.datetime | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    organization: TeamRestObject | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    standings_type: str | Unset = UNSET
    team_records: list[TeamStandingsRecordRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.team_standings_record_rest_object import (
            TeamStandingsRecordRestObject,
        )

        aggregate_record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.aggregate_record, Unset):
            aggregate_record = self.aggregate_record.to_dict()

        conference: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conference, Unset):
            conference = self.conference.to_dict()

        division: dict[str, Any] | Unset = UNSET
        if not isinstance(self.division, Unset):
            division = self.division.to_dict()

        last_updated: str | Unset = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        organization: dict[str, Any] | Unset = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        standings_type = self.standings_type

        team_records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.team_records, Unset):
            team_records = []
            for team_records_item_data in self.team_records:
                team_records_item = team_records_item_data.to_dict()
                team_records.append(team_records_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregate_record is not UNSET:
            field_dict["aggregateRecord"] = aggregate_record
        if conference is not UNSET:
            field_dict["conference"] = conference
        if division is not UNSET:
            field_dict["division"] = division
        if last_updated is not UNSET:
            field_dict["lastUpdated"] = last_updated
        if league is not UNSET:
            field_dict["league"] = league
        if organization is not UNSET:
            field_dict["organization"] = organization
        if sport is not UNSET:
            field_dict["sport"] = sport
        if standings_type is not UNSET:
            field_dict["standingsType"] = standings_type
        if team_records is not UNSET:
            field_dict["teamRecords"] = team_records

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.team_standings_record_rest_object import (
            TeamStandingsRecordRestObject,
        )

        d = dict(src_dict)
        _aggregate_record = d.pop("aggregateRecord", UNSET)
        aggregate_record: TeamStandingsRecordRestObject | Unset
        if isinstance(_aggregate_record, Unset):
            aggregate_record = UNSET
        else:
            aggregate_record = TeamStandingsRecordRestObject.from_dict(
                _aggregate_record
            )

        _conference = d.pop("conference", UNSET)
        conference: ConferenceRestObject | Unset
        if isinstance(_conference, Unset):
            conference = UNSET
        else:
            conference = ConferenceRestObject.from_dict(_conference)

        _division = d.pop("division", UNSET)
        division: DivisionRestObject | Unset
        if isinstance(_division, Unset):
            division = UNSET
        else:
            division = DivisionRestObject.from_dict(_division)

        _last_updated = d.pop("lastUpdated", UNSET)
        last_updated: datetime.datetime | Unset
        if isinstance(_last_updated, Unset):
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        _organization = d.pop("organization", UNSET)
        organization: TeamRestObject | Unset
        if isinstance(_organization, Unset):
            organization = UNSET
        else:
            organization = TeamRestObject.from_dict(_organization)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        standings_type = d.pop("standingsType", UNSET)

        _team_records = d.pop("teamRecords", UNSET)
        team_records: list[TeamStandingsRecordRestObject] | Unset = UNSET
        if _team_records is not UNSET:
            team_records = []
            for team_records_item_data in _team_records:
                team_records_item = TeamStandingsRecordRestObject.from_dict(
                    team_records_item_data
                )

                team_records.append(team_records_item)

        team_standings_record_container_rest_object = cls(
            aggregate_record=aggregate_record,
            conference=conference,
            division=division,
            last_updated=last_updated,
            league=league,
            organization=organization,
            sport=sport,
            standings_type=standings_type,
            team_records=team_records,
        )

        team_standings_record_container_rest_object.additional_properties = d
        return team_standings_record_container_rest_object

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
