from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conference_rest_object import ConferenceRestObject
    from ..models.division_rest_object import DivisionRestObject
    from ..models.franchise_rest_object import FranchiseRestObject
    from ..models.leaders_rest_object import LeadersRestObject
    from ..models.league_rest_object import LeagueRestObject
    from ..models.roster_rest_object import RosterRestObject
    from ..models.social_media_rest_object import SocialMediaRestObject
    from ..models.sport_rest_object import SportRestObject
    from ..models.stat_container_rest_object import StatContainerRestObject
    from ..models.team_standings_record_rest_object import TeamStandingsRecordRestObject
    from ..models.venue_rest_object import VenueRestObject


T = TypeVar("T", bound="TeamRestObject")


@_attrs_define
class TeamRestObject:
    """
    Attributes:
        abbreviation (str | Unset): Shortened version of short name. Format: ALE, SFG
        conference (ConferenceRestObject | Unset):
        content (Any | Unset):
        device_properties (Any | Unset):
        division (DivisionRestObject | Unset):
        file_code (str | Unset): Unique File Code. Format: tor, nyy, etc
        first_year_of_play (str | Unset): The first year of play. Format: 1903
        franchise (FranchiseRestObject | Unset):
        id (int | Unset): Unique Team Identifier. Format: 141, 147, etc
        is_active (bool | Unset):
        is_placeholder (bool | Unset):
        league (LeagueRestObject | Unset):
        link (str | Unset): Link to full resource
        location_name (str | Unset): Unique Team Location. Toronto, Bronx, etc
        name (str | Unset): Unique Full Team Name. Format: Toronto Blue Jays, New York Yankees, etc
        next_game_schedule (Any | Unset):
        next_schedule (Any | Unset):
        parent_org_id (int | Unset):
        parent_org_name (str | Unset):
        playoff_info (Any | Unset):
        previous_game_schedule (Any | Unset):
        previous_schedule (Any | Unset):
        record (TeamStandingsRecordRestObject | Unset):
        roster (RosterRestObject | Unset):
        season (int | Unset): Season of play
        short_name (str | Unset): Shortened version of name. Format: AL East, SF Giants
        social (SocialMediaRestObject | Unset):
        sport (SportRestObject | Unset):
        spring_venue (VenueRestObject | Unset):
        team_code (str | Unset): Unique Team Code. Format: tor, nya, etc
        team_leaders (list[LeadersRestObject] | Unset): All of the details of team leaders
        team_name (str | Unset): Unique Team Name. Blue Jays, Yankees, etc
        team_stats (list[StatContainerRestObject] | Unset): All of the details of a player's stats
        tri_code (str | Unset): Three letter abbreviation that will be adjusted for different languages
        venue (VenueRestObject | Unset):
    """

    abbreviation: str | Unset = UNSET
    conference: ConferenceRestObject | Unset = UNSET
    content: Any | Unset = UNSET
    device_properties: Any | Unset = UNSET
    division: DivisionRestObject | Unset = UNSET
    file_code: str | Unset = UNSET
    first_year_of_play: str | Unset = UNSET
    franchise: FranchiseRestObject | Unset = UNSET
    id: int | Unset = UNSET
    is_active: bool | Unset = UNSET
    is_placeholder: bool | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    link: str | Unset = UNSET
    location_name: str | Unset = UNSET
    name: str | Unset = UNSET
    next_game_schedule: Any | Unset = UNSET
    next_schedule: Any | Unset = UNSET
    parent_org_id: int | Unset = UNSET
    parent_org_name: str | Unset = UNSET
    playoff_info: Any | Unset = UNSET
    previous_game_schedule: Any | Unset = UNSET
    previous_schedule: Any | Unset = UNSET
    record: TeamStandingsRecordRestObject | Unset = UNSET
    roster: RosterRestObject | Unset = UNSET
    season: int | Unset = UNSET
    short_name: str | Unset = UNSET
    social: SocialMediaRestObject | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    spring_venue: VenueRestObject | Unset = UNSET
    team_code: str | Unset = UNSET
    team_leaders: list[LeadersRestObject] | Unset = UNSET
    team_name: str | Unset = UNSET
    team_stats: list[StatContainerRestObject] | Unset = UNSET
    tri_code: str | Unset = UNSET
    venue: VenueRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.franchise_rest_object import FranchiseRestObject
        from ..models.leaders_rest_object import LeadersRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.roster_rest_object import RosterRestObject
        from ..models.social_media_rest_object import SocialMediaRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.stat_container_rest_object import StatContainerRestObject
        from ..models.team_standings_record_rest_object import (
            TeamStandingsRecordRestObject,
        )
        from ..models.venue_rest_object import VenueRestObject

        abbreviation = self.abbreviation

        conference: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conference, Unset):
            conference = self.conference.to_dict()

        content = self.content

        device_properties = self.device_properties

        division: dict[str, Any] | Unset = UNSET
        if not isinstance(self.division, Unset):
            division = self.division.to_dict()

        file_code = self.file_code

        first_year_of_play = self.first_year_of_play

        franchise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.franchise, Unset):
            franchise = self.franchise.to_dict()

        id = self.id

        is_active = self.is_active

        is_placeholder = self.is_placeholder

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        link = self.link

        location_name = self.location_name

        name = self.name

        next_game_schedule = self.next_game_schedule

        next_schedule = self.next_schedule

        parent_org_id = self.parent_org_id

        parent_org_name = self.parent_org_name

        playoff_info = self.playoff_info

        previous_game_schedule = self.previous_game_schedule

        previous_schedule = self.previous_schedule

        record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.record, Unset):
            record = self.record.to_dict()

        roster: dict[str, Any] | Unset = UNSET
        if not isinstance(self.roster, Unset):
            roster = self.roster.to_dict()

        season = self.season

        short_name = self.short_name

        social: dict[str, Any] | Unset = UNSET
        if not isinstance(self.social, Unset):
            social = self.social.to_dict()

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        spring_venue: dict[str, Any] | Unset = UNSET
        if not isinstance(self.spring_venue, Unset):
            spring_venue = self.spring_venue.to_dict()

        team_code = self.team_code

        team_leaders: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.team_leaders, Unset):
            team_leaders = []
            for team_leaders_item_data in self.team_leaders:
                team_leaders_item = team_leaders_item_data.to_dict()
                team_leaders.append(team_leaders_item)

        team_name = self.team_name

        team_stats: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.team_stats, Unset):
            team_stats = []
            for team_stats_item_data in self.team_stats:
                team_stats_item = team_stats_item_data.to_dict()
                team_stats.append(team_stats_item)

        tri_code = self.tri_code

        venue: dict[str, Any] | Unset = UNSET
        if not isinstance(self.venue, Unset):
            venue = self.venue.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if abbreviation is not UNSET:
            field_dict["abbreviation"] = abbreviation
        if conference is not UNSET:
            field_dict["conference"] = conference
        if content is not UNSET:
            field_dict["content"] = content
        if device_properties is not UNSET:
            field_dict["deviceProperties"] = device_properties
        if division is not UNSET:
            field_dict["division"] = division
        if file_code is not UNSET:
            field_dict["fileCode"] = file_code
        if first_year_of_play is not UNSET:
            field_dict["firstYearOfPlay"] = first_year_of_play
        if franchise is not UNSET:
            field_dict["franchise"] = franchise
        if id is not UNSET:
            field_dict["id"] = id
        if is_active is not UNSET:
            field_dict["isActive"] = is_active
        if is_placeholder is not UNSET:
            field_dict["isPlaceholder"] = is_placeholder
        if league is not UNSET:
            field_dict["league"] = league
        if link is not UNSET:
            field_dict["link"] = link
        if location_name is not UNSET:
            field_dict["locationName"] = location_name
        if name is not UNSET:
            field_dict["name"] = name
        if next_game_schedule is not UNSET:
            field_dict["nextGameSchedule"] = next_game_schedule
        if next_schedule is not UNSET:
            field_dict["nextSchedule"] = next_schedule
        if parent_org_id is not UNSET:
            field_dict["parentOrgId"] = parent_org_id
        if parent_org_name is not UNSET:
            field_dict["parentOrgName"] = parent_org_name
        if playoff_info is not UNSET:
            field_dict["playoffInfo"] = playoff_info
        if previous_game_schedule is not UNSET:
            field_dict["previousGameSchedule"] = previous_game_schedule
        if previous_schedule is not UNSET:
            field_dict["previousSchedule"] = previous_schedule
        if record is not UNSET:
            field_dict["record"] = record
        if roster is not UNSET:
            field_dict["roster"] = roster
        if season is not UNSET:
            field_dict["season"] = season
        if short_name is not UNSET:
            field_dict["shortName"] = short_name
        if social is not UNSET:
            field_dict["social"] = social
        if sport is not UNSET:
            field_dict["sport"] = sport
        if spring_venue is not UNSET:
            field_dict["springVenue"] = spring_venue
        if team_code is not UNSET:
            field_dict["teamCode"] = team_code
        if team_leaders is not UNSET:
            field_dict["teamLeaders"] = team_leaders
        if team_name is not UNSET:
            field_dict["teamName"] = team_name
        if team_stats is not UNSET:
            field_dict["teamStats"] = team_stats
        if tri_code is not UNSET:
            field_dict["triCode"] = tri_code
        if venue is not UNSET:
            field_dict["venue"] = venue

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conference_rest_object import ConferenceRestObject
        from ..models.division_rest_object import DivisionRestObject
        from ..models.franchise_rest_object import FranchiseRestObject
        from ..models.leaders_rest_object import LeadersRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.roster_rest_object import RosterRestObject
        from ..models.social_media_rest_object import SocialMediaRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.stat_container_rest_object import StatContainerRestObject
        from ..models.team_standings_record_rest_object import (
            TeamStandingsRecordRestObject,
        )
        from ..models.venue_rest_object import VenueRestObject

        d = dict(src_dict)
        abbreviation = d.pop("abbreviation", UNSET)

        _conference = d.pop("conference", UNSET)
        conference: ConferenceRestObject | Unset
        if isinstance(_conference, Unset):
            conference = UNSET
        else:
            conference = ConferenceRestObject.from_dict(_conference)

        content = d.pop("content", UNSET)

        device_properties = d.pop("deviceProperties", UNSET)

        _division = d.pop("division", UNSET)
        division: DivisionRestObject | Unset
        if isinstance(_division, Unset):
            division = UNSET
        else:
            division = DivisionRestObject.from_dict(_division)

        file_code = d.pop("fileCode", UNSET)

        first_year_of_play = d.pop("firstYearOfPlay", UNSET)

        _franchise = d.pop("franchise", UNSET)
        franchise: FranchiseRestObject | Unset
        if isinstance(_franchise, Unset):
            franchise = UNSET
        else:
            franchise = FranchiseRestObject.from_dict(_franchise)

        id = d.pop("id", UNSET)

        is_active = d.pop("isActive", UNSET)

        is_placeholder = d.pop("isPlaceholder", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        link = d.pop("link", UNSET)

        location_name = d.pop("locationName", UNSET)

        name = d.pop("name", UNSET)

        next_game_schedule = d.pop("nextGameSchedule", UNSET)

        next_schedule = d.pop("nextSchedule", UNSET)

        parent_org_id = d.pop("parentOrgId", UNSET)

        parent_org_name = d.pop("parentOrgName", UNSET)

        playoff_info = d.pop("playoffInfo", UNSET)

        previous_game_schedule = d.pop("previousGameSchedule", UNSET)

        previous_schedule = d.pop("previousSchedule", UNSET)

        _record = d.pop("record", UNSET)
        record: TeamStandingsRecordRestObject | Unset
        if isinstance(_record, Unset):
            record = UNSET
        else:
            record = TeamStandingsRecordRestObject.from_dict(_record)

        _roster = d.pop("roster", UNSET)
        roster: RosterRestObject | Unset
        if isinstance(_roster, Unset):
            roster = UNSET
        else:
            roster = RosterRestObject.from_dict(_roster)

        season = d.pop("season", UNSET)

        short_name = d.pop("shortName", UNSET)

        _social = d.pop("social", UNSET)
        social: SocialMediaRestObject | Unset
        if isinstance(_social, Unset):
            social = UNSET
        else:
            social = SocialMediaRestObject.from_dict(_social)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        _spring_venue = d.pop("springVenue", UNSET)
        spring_venue: VenueRestObject | Unset
        if isinstance(_spring_venue, Unset):
            spring_venue = UNSET
        else:
            spring_venue = VenueRestObject.from_dict(_spring_venue)

        team_code = d.pop("teamCode", UNSET)

        _team_leaders = d.pop("teamLeaders", UNSET)
        team_leaders: list[LeadersRestObject] | Unset = UNSET
        if _team_leaders is not UNSET:
            team_leaders = []
            for team_leaders_item_data in _team_leaders:
                team_leaders_item = LeadersRestObject.from_dict(team_leaders_item_data)

                team_leaders.append(team_leaders_item)

        team_name = d.pop("teamName", UNSET)

        _team_stats = d.pop("teamStats", UNSET)
        team_stats: list[StatContainerRestObject] | Unset = UNSET
        if _team_stats is not UNSET:
            team_stats = []
            for team_stats_item_data in _team_stats:
                team_stats_item = StatContainerRestObject.from_dict(
                    team_stats_item_data
                )

                team_stats.append(team_stats_item)

        tri_code = d.pop("triCode", UNSET)

        _venue = d.pop("venue", UNSET)
        venue: VenueRestObject | Unset
        if isinstance(_venue, Unset):
            venue = UNSET
        else:
            venue = VenueRestObject.from_dict(_venue)

        team_rest_object = cls(
            abbreviation=abbreviation,
            conference=conference,
            content=content,
            device_properties=device_properties,
            division=division,
            file_code=file_code,
            first_year_of_play=first_year_of_play,
            franchise=franchise,
            id=id,
            is_active=is_active,
            is_placeholder=is_placeholder,
            league=league,
            link=link,
            location_name=location_name,
            name=name,
            next_game_schedule=next_game_schedule,
            next_schedule=next_schedule,
            parent_org_id=parent_org_id,
            parent_org_name=parent_org_name,
            playoff_info=playoff_info,
            previous_game_schedule=previous_game_schedule,
            previous_schedule=previous_schedule,
            record=record,
            roster=roster,
            season=season,
            short_name=short_name,
            social=social,
            sport=sport,
            spring_venue=spring_venue,
            team_code=team_code,
            team_leaders=team_leaders,
            team_name=team_name,
            team_stats=team_stats,
            tri_code=tri_code,
            venue=venue,
        )

        team_rest_object.additional_properties = d
        return team_rest_object

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
