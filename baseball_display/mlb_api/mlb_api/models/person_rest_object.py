from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_rest_object import AwardRestObject
    from ..models.education_rest_object import EducationRestObject
    from ..models.other_names_rest_object import OtherNamesRestObject
    from ..models.player_draft_info_rest_object import PlayerDraftInfoRestObject
    from ..models.position_rest_object import PositionRestObject
    from ..models.roster_entry_rest_object import RosterEntryRestObject
    from ..models.social_media_rest_object import SocialMediaRestObject
    from ..models.stat_container_rest_object import StatContainerRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="PersonRestObject")


@_attrs_define
class PersonRestObject:
    """
    Attributes:
        active (bool | Unset): Whether or not a player is active
        additional_bio (Any | Unset):
        alternate_captain (bool | Unset): Whether or not a player is an alternate captain
        awards (list[AwardRestObject] | Unset): All of the details of a player's awards
        birth_city (str | Unset): City the player was born in. Format: La Romana
        birth_country (str | Unset): Country the player was born in. Format: Dominican Republic
        birth_date (datetime.date | Unset): Birth date of a player. Format: 1983-01-07
        birth_state_province (str | Unset): State or Province the player was born in. Format: NY
        boxscore_name (str | Unset): Name that shows up in the box score. Last name or last name and first initial
        captain (bool | Unset): Whether or not a player is a captain
        current_age (int | Unset): Current age of a player. Format: 34
        current_team (TeamRestObject | Unset):
        death_city (str | Unset): City the player died in. Format: La Romana
        death_country (str | Unset): Country the player died in. Format: Dominican Republic
        death_date (datetime.date | Unset): Death date of a player. Format: 1983-01-07
        death_state_province (str | Unset): State or Province the player died in. Format: NY
        draft (list[PlayerDraftInfoRestObject] | Unset): All of the details of the draft a player was drafted in
        draft_year (int | Unset): Year the player was drafted. Format: 2000
        education (EducationRestObject | Unset):
        first_name (str | Unset): First name of a player
        full_name (str | Unset): Full name of a player. Format: Edwin Encarnacion
        height (str | Unset): Height of a player. Format: 6' 1
        id (int | Unset): Unique Player Identifier. Format: 434538, 429665, etc
        last_name (str | Unset): Last name of a player
        last_played_date (datetime.date | Unset): Date of last game played. Format: 1983-01-07
        link (str | Unset): Link to full resource
        middle_name (str | Unset): Middle name of a player
        nationality (str | Unset):
        nick_name (str | Unset): Nick nme for a player. Example: The Freak
        other_names (OtherNamesRestObject | Unset):
        photos (list[Any] | Unset): Links to images of person.
        primary_number (str | Unset): The jersey number a player wears
        primary_position (PositionRestObject | Unset):
        pronunciation (str | Unset): Pronunciation guide for a player's name
        rookie (bool | Unset): Whether or not a player is a rookie
        roster_entries (list[RosterEntryRestObject] | Unset):
        social (SocialMediaRestObject | Unset):
        stats (list[StatContainerRestObject] | Unset): All of the details of a player's stats
        use_name (str | Unset): Name a player uses
        weight (int | Unset): Weight of a player. Format: 230
    """

    active: bool | Unset = UNSET
    additional_bio: Any | Unset = UNSET
    alternate_captain: bool | Unset = UNSET
    awards: list[AwardRestObject] | Unset = UNSET
    birth_city: str | Unset = UNSET
    birth_country: str | Unset = UNSET
    birth_date: datetime.date | Unset = UNSET
    birth_state_province: str | Unset = UNSET
    boxscore_name: str | Unset = UNSET
    captain: bool | Unset = UNSET
    current_age: int | Unset = UNSET
    current_team: TeamRestObject | Unset = UNSET
    death_city: str | Unset = UNSET
    death_country: str | Unset = UNSET
    death_date: datetime.date | Unset = UNSET
    death_state_province: str | Unset = UNSET
    draft: list[PlayerDraftInfoRestObject] | Unset = UNSET
    draft_year: int | Unset = UNSET
    education: EducationRestObject | Unset = UNSET
    first_name: str | Unset = UNSET
    full_name: str | Unset = UNSET
    height: str | Unset = UNSET
    id: int | Unset = UNSET
    last_name: str | Unset = UNSET
    last_played_date: datetime.date | Unset = UNSET
    link: str | Unset = UNSET
    middle_name: str | Unset = UNSET
    nationality: str | Unset = UNSET
    nick_name: str | Unset = UNSET
    other_names: OtherNamesRestObject | Unset = UNSET
    photos: list[Any] | Unset = UNSET
    primary_number: str | Unset = UNSET
    primary_position: PositionRestObject | Unset = UNSET
    pronunciation: str | Unset = UNSET
    rookie: bool | Unset = UNSET
    roster_entries: list[RosterEntryRestObject] | Unset = UNSET
    social: SocialMediaRestObject | Unset = UNSET
    stats: list[StatContainerRestObject] | Unset = UNSET
    use_name: str | Unset = UNSET
    weight: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_rest_object import AwardRestObject
        from ..models.education_rest_object import EducationRestObject
        from ..models.other_names_rest_object import OtherNamesRestObject
        from ..models.player_draft_info_rest_object import PlayerDraftInfoRestObject
        from ..models.position_rest_object import PositionRestObject
        from ..models.roster_entry_rest_object import RosterEntryRestObject
        from ..models.social_media_rest_object import SocialMediaRestObject
        from ..models.stat_container_rest_object import StatContainerRestObject
        from ..models.team_rest_object import TeamRestObject

        active = self.active

        additional_bio = self.additional_bio

        alternate_captain = self.alternate_captain

        awards: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.awards, Unset):
            awards = []
            for awards_item_data in self.awards:
                awards_item = awards_item_data.to_dict()
                awards.append(awards_item)

        birth_city = self.birth_city

        birth_country = self.birth_country

        birth_date: str | Unset = UNSET
        if not isinstance(self.birth_date, Unset):
            birth_date = self.birth_date.isoformat()

        birth_state_province = self.birth_state_province

        boxscore_name = self.boxscore_name

        captain = self.captain

        current_age = self.current_age

        current_team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.current_team, Unset):
            current_team = self.current_team.to_dict()

        death_city = self.death_city

        death_country = self.death_country

        death_date: str | Unset = UNSET
        if not isinstance(self.death_date, Unset):
            death_date = self.death_date.isoformat()

        death_state_province = self.death_state_province

        draft: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.draft, Unset):
            draft = []
            for draft_item_data in self.draft:
                draft_item = draft_item_data.to_dict()
                draft.append(draft_item)

        draft_year = self.draft_year

        education: dict[str, Any] | Unset = UNSET
        if not isinstance(self.education, Unset):
            education = self.education.to_dict()

        first_name = self.first_name

        full_name = self.full_name

        height = self.height

        id = self.id

        last_name = self.last_name

        last_played_date: str | Unset = UNSET
        if not isinstance(self.last_played_date, Unset):
            last_played_date = self.last_played_date.isoformat()

        link = self.link

        middle_name = self.middle_name

        nationality = self.nationality

        nick_name = self.nick_name

        other_names: dict[str, Any] | Unset = UNSET
        if not isinstance(self.other_names, Unset):
            other_names = self.other_names.to_dict()

        photos: list[Any] | Unset = UNSET
        if not isinstance(self.photos, Unset):
            photos = self.photos

        primary_number = self.primary_number

        primary_position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.primary_position, Unset):
            primary_position = self.primary_position.to_dict()

        pronunciation = self.pronunciation

        rookie = self.rookie

        roster_entries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.roster_entries, Unset):
            roster_entries = []
            for roster_entries_item_data in self.roster_entries:
                roster_entries_item = roster_entries_item_data.to_dict()
                roster_entries.append(roster_entries_item)

        social: dict[str, Any] | Unset = UNSET
        if not isinstance(self.social, Unset):
            social = self.social.to_dict()

        stats: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = []
            for stats_item_data in self.stats:
                stats_item = stats_item_data.to_dict()
                stats.append(stats_item)

        use_name = self.use_name

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if additional_bio is not UNSET:
            field_dict["additionalBio"] = additional_bio
        if alternate_captain is not UNSET:
            field_dict["alternateCaptain"] = alternate_captain
        if awards is not UNSET:
            field_dict["awards"] = awards
        if birth_city is not UNSET:
            field_dict["birthCity"] = birth_city
        if birth_country is not UNSET:
            field_dict["birthCountry"] = birth_country
        if birth_date is not UNSET:
            field_dict["birthDate"] = birth_date
        if birth_state_province is not UNSET:
            field_dict["birthStateProvince"] = birth_state_province
        if boxscore_name is not UNSET:
            field_dict["boxscoreName"] = boxscore_name
        if captain is not UNSET:
            field_dict["captain"] = captain
        if current_age is not UNSET:
            field_dict["currentAge"] = current_age
        if current_team is not UNSET:
            field_dict["currentTeam"] = current_team
        if death_city is not UNSET:
            field_dict["deathCity"] = death_city
        if death_country is not UNSET:
            field_dict["deathCountry"] = death_country
        if death_date is not UNSET:
            field_dict["deathDate"] = death_date
        if death_state_province is not UNSET:
            field_dict["deathStateProvince"] = death_state_province
        if draft is not UNSET:
            field_dict["draft"] = draft
        if draft_year is not UNSET:
            field_dict["draftYear"] = draft_year
        if education is not UNSET:
            field_dict["education"] = education
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if height is not UNSET:
            field_dict["height"] = height
        if id is not UNSET:
            field_dict["id"] = id
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if last_played_date is not UNSET:
            field_dict["lastPlayedDate"] = last_played_date
        if link is not UNSET:
            field_dict["link"] = link
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if nick_name is not UNSET:
            field_dict["nickName"] = nick_name
        if other_names is not UNSET:
            field_dict["otherNames"] = other_names
        if photos is not UNSET:
            field_dict["photos"] = photos
        if primary_number is not UNSET:
            field_dict["primaryNumber"] = primary_number
        if primary_position is not UNSET:
            field_dict["primaryPosition"] = primary_position
        if pronunciation is not UNSET:
            field_dict["pronunciation"] = pronunciation
        if rookie is not UNSET:
            field_dict["rookie"] = rookie
        if roster_entries is not UNSET:
            field_dict["rosterEntries"] = roster_entries
        if social is not UNSET:
            field_dict["social"] = social
        if stats is not UNSET:
            field_dict["stats"] = stats
        if use_name is not UNSET:
            field_dict["useName"] = use_name
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_rest_object import AwardRestObject
        from ..models.education_rest_object import EducationRestObject
        from ..models.other_names_rest_object import OtherNamesRestObject
        from ..models.player_draft_info_rest_object import PlayerDraftInfoRestObject
        from ..models.position_rest_object import PositionRestObject
        from ..models.roster_entry_rest_object import RosterEntryRestObject
        from ..models.social_media_rest_object import SocialMediaRestObject
        from ..models.stat_container_rest_object import StatContainerRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        active = d.pop("active", UNSET)

        additional_bio = d.pop("additionalBio", UNSET)

        alternate_captain = d.pop("alternateCaptain", UNSET)

        _awards = d.pop("awards", UNSET)
        awards: list[AwardRestObject] | Unset = UNSET
        if _awards is not UNSET:
            awards = []
            for awards_item_data in _awards:
                awards_item = AwardRestObject.from_dict(awards_item_data)

                awards.append(awards_item)

        birth_city = d.pop("birthCity", UNSET)

        birth_country = d.pop("birthCountry", UNSET)

        _birth_date = d.pop("birthDate", UNSET)
        birth_date: datetime.date | Unset
        if isinstance(_birth_date, Unset):
            birth_date = UNSET
        else:
            birth_date = isoparse(_birth_date).date()

        birth_state_province = d.pop("birthStateProvince", UNSET)

        boxscore_name = d.pop("boxscoreName", UNSET)

        captain = d.pop("captain", UNSET)

        current_age = d.pop("currentAge", UNSET)

        _current_team = d.pop("currentTeam", UNSET)
        current_team: TeamRestObject | Unset
        if isinstance(_current_team, Unset):
            current_team = UNSET
        else:
            current_team = TeamRestObject.from_dict(_current_team)

        death_city = d.pop("deathCity", UNSET)

        death_country = d.pop("deathCountry", UNSET)

        _death_date = d.pop("deathDate", UNSET)
        death_date: datetime.date | Unset
        if isinstance(_death_date, Unset):
            death_date = UNSET
        else:
            death_date = isoparse(_death_date).date()

        death_state_province = d.pop("deathStateProvince", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: list[PlayerDraftInfoRestObject] | Unset = UNSET
        if _draft is not UNSET:
            draft = []
            for draft_item_data in _draft:
                draft_item = PlayerDraftInfoRestObject.from_dict(draft_item_data)

                draft.append(draft_item)

        draft_year = d.pop("draftYear", UNSET)

        _education = d.pop("education", UNSET)
        education: EducationRestObject | Unset
        if isinstance(_education, Unset):
            education = UNSET
        else:
            education = EducationRestObject.from_dict(_education)

        first_name = d.pop("firstName", UNSET)

        full_name = d.pop("fullName", UNSET)

        height = d.pop("height", UNSET)

        id = d.pop("id", UNSET)

        last_name = d.pop("lastName", UNSET)

        _last_played_date = d.pop("lastPlayedDate", UNSET)
        last_played_date: datetime.date | Unset
        if isinstance(_last_played_date, Unset):
            last_played_date = UNSET
        else:
            last_played_date = isoparse(_last_played_date).date()

        link = d.pop("link", UNSET)

        middle_name = d.pop("middleName", UNSET)

        nationality = d.pop("nationality", UNSET)

        nick_name = d.pop("nickName", UNSET)

        _other_names = d.pop("otherNames", UNSET)
        other_names: OtherNamesRestObject | Unset
        if isinstance(_other_names, Unset):
            other_names = UNSET
        else:
            other_names = OtherNamesRestObject.from_dict(_other_names)

        photos = cast(list[Any], d.pop("photos", UNSET))

        primary_number = d.pop("primaryNumber", UNSET)

        _primary_position = d.pop("primaryPosition", UNSET)
        primary_position: PositionRestObject | Unset
        if isinstance(_primary_position, Unset):
            primary_position = UNSET
        else:
            primary_position = PositionRestObject.from_dict(_primary_position)

        pronunciation = d.pop("pronunciation", UNSET)

        rookie = d.pop("rookie", UNSET)

        _roster_entries = d.pop("rosterEntries", UNSET)
        roster_entries: list[RosterEntryRestObject] | Unset = UNSET
        if _roster_entries is not UNSET:
            roster_entries = []
            for roster_entries_item_data in _roster_entries:
                roster_entries_item = RosterEntryRestObject.from_dict(
                    roster_entries_item_data
                )

                roster_entries.append(roster_entries_item)

        _social = d.pop("social", UNSET)
        social: SocialMediaRestObject | Unset
        if isinstance(_social, Unset):
            social = UNSET
        else:
            social = SocialMediaRestObject.from_dict(_social)

        _stats = d.pop("stats", UNSET)
        stats: list[StatContainerRestObject] | Unset = UNSET
        if _stats is not UNSET:
            stats = []
            for stats_item_data in _stats:
                stats_item = StatContainerRestObject.from_dict(stats_item_data)

                stats.append(stats_item)

        use_name = d.pop("useName", UNSET)

        weight = d.pop("weight", UNSET)

        person_rest_object = cls(
            active=active,
            additional_bio=additional_bio,
            alternate_captain=alternate_captain,
            awards=awards,
            birth_city=birth_city,
            birth_country=birth_country,
            birth_date=birth_date,
            birth_state_province=birth_state_province,
            boxscore_name=boxscore_name,
            captain=captain,
            current_age=current_age,
            current_team=current_team,
            death_city=death_city,
            death_country=death_country,
            death_date=death_date,
            death_state_province=death_state_province,
            draft=draft,
            draft_year=draft_year,
            education=education,
            first_name=first_name,
            full_name=full_name,
            height=height,
            id=id,
            last_name=last_name,
            last_played_date=last_played_date,
            link=link,
            middle_name=middle_name,
            nationality=nationality,
            nick_name=nick_name,
            other_names=other_names,
            photos=photos,
            primary_number=primary_number,
            primary_position=primary_position,
            pronunciation=pronunciation,
            rookie=rookie,
            roster_entries=roster_entries,
            social=social,
            stats=stats,
            use_name=use_name,
            weight=weight,
        )

        person_rest_object.additional_properties = d
        return person_rest_object

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
