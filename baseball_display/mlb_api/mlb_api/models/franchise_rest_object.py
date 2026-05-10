from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.roster_rest_object import RosterRestObject


T = TypeVar("T", bound="FranchiseRestObject")


@_attrs_define
class FranchiseRestObject:
    """
    Attributes:
        first_season_id (int | Unset):
        franchise_id (int | Unset):
        last_season_id (int | Unset):
        link (str | Unset):
        location_name (str | Unset):
        most_recent_team_id (int | Unset):
        roster (RosterRestObject | Unset):
        team_name (str | Unset):
    """

    first_season_id: int | Unset = UNSET
    franchise_id: int | Unset = UNSET
    last_season_id: int | Unset = UNSET
    link: str | Unset = UNSET
    location_name: str | Unset = UNSET
    most_recent_team_id: int | Unset = UNSET
    roster: RosterRestObject | Unset = UNSET
    team_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.roster_rest_object import RosterRestObject

        first_season_id = self.first_season_id

        franchise_id = self.franchise_id

        last_season_id = self.last_season_id

        link = self.link

        location_name = self.location_name

        most_recent_team_id = self.most_recent_team_id

        roster: dict[str, Any] | Unset = UNSET
        if not isinstance(self.roster, Unset):
            roster = self.roster.to_dict()

        team_name = self.team_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_season_id is not UNSET:
            field_dict["firstSeasonId"] = first_season_id
        if franchise_id is not UNSET:
            field_dict["franchiseId"] = franchise_id
        if last_season_id is not UNSET:
            field_dict["lastSeasonId"] = last_season_id
        if link is not UNSET:
            field_dict["link"] = link
        if location_name is not UNSET:
            field_dict["locationName"] = location_name
        if most_recent_team_id is not UNSET:
            field_dict["mostRecentTeamId"] = most_recent_team_id
        if roster is not UNSET:
            field_dict["roster"] = roster
        if team_name is not UNSET:
            field_dict["teamName"] = team_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.roster_rest_object import RosterRestObject

        d = dict(src_dict)
        first_season_id = d.pop("firstSeasonId", UNSET)

        franchise_id = d.pop("franchiseId", UNSET)

        last_season_id = d.pop("lastSeasonId", UNSET)

        link = d.pop("link", UNSET)

        location_name = d.pop("locationName", UNSET)

        most_recent_team_id = d.pop("mostRecentTeamId", UNSET)

        _roster = d.pop("roster", UNSET)
        roster: RosterRestObject | Unset
        if isinstance(_roster, Unset):
            roster = UNSET
        else:
            roster = RosterRestObject.from_dict(_roster)

        team_name = d.pop("teamName", UNSET)

        franchise_rest_object = cls(
            first_season_id=first_season_id,
            franchise_id=franchise_id,
            last_season_id=last_season_id,
            link=link,
            location_name=location_name,
            most_recent_team_id=most_recent_team_id,
            roster=roster,
            team_name=team_name,
        )

        franchise_rest_object.additional_properties = d
        return franchise_rest_object

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
