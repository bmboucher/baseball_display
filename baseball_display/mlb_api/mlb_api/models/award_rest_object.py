from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_result_rest_object import AwardResultRestObject
    from ..models.baseball_person_rest_object import BaseballPersonRestObject
    from ..models.league_rest_object import LeagueRestObject
    from ..models.sport_rest_object import SportRestObject
    from ..models.team_rest_object import TeamRestObject


T = TypeVar("T", bound="AwardRestObject")


@_attrs_define
class AwardRestObject:
    """
    Attributes:
        date (datetime.date | Unset):
        description (str | Unset):
        history (str | Unset):
        home_page_url (str | Unset):
        id (str | Unset):
        image_url (str | Unset):
        league (LeagueRestObject | Unset):
        name (str | Unset):
        notes (str | Unset):
        player (BaseballPersonRestObject | Unset):
        recipient_type (str | Unset):
        results (list[AwardResultRestObject] | Unset):
        season (str | Unset):
        short_name (str | Unset):
        sort_order (int | Unset):
        sport (SportRestObject | Unset):
        team (TeamRestObject | Unset):
        votes (int | Unset):
    """

    date: datetime.date | Unset = UNSET
    description: str | Unset = UNSET
    history: str | Unset = UNSET
    home_page_url: str | Unset = UNSET
    id: str | Unset = UNSET
    image_url: str | Unset = UNSET
    league: LeagueRestObject | Unset = UNSET
    name: str | Unset = UNSET
    notes: str | Unset = UNSET
    player: BaseballPersonRestObject | Unset = UNSET
    recipient_type: str | Unset = UNSET
    results: list[AwardResultRestObject] | Unset = UNSET
    season: str | Unset = UNSET
    short_name: str | Unset = UNSET
    sort_order: int | Unset = UNSET
    sport: SportRestObject | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    votes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_result_rest_object import AwardResultRestObject
        from ..models.baseball_person_rest_object import BaseballPersonRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject

        date: str | Unset = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        description = self.description

        history = self.history

        home_page_url = self.home_page_url

        id = self.id

        image_url = self.image_url

        league: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league, Unset):
            league = self.league.to_dict()

        name = self.name

        notes = self.notes

        player: dict[str, Any] | Unset = UNSET
        if not isinstance(self.player, Unset):
            player = self.player.to_dict()

        recipient_type = self.recipient_type

        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        season = self.season

        short_name = self.short_name

        sort_order = self.sort_order

        sport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sport, Unset):
            sport = self.sport.to_dict()

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        votes = self.votes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if description is not UNSET:
            field_dict["description"] = description
        if history is not UNSET:
            field_dict["history"] = history
        if home_page_url is not UNSET:
            field_dict["homePageUrl"] = home_page_url
        if id is not UNSET:
            field_dict["id"] = id
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if league is not UNSET:
            field_dict["league"] = league
        if name is not UNSET:
            field_dict["name"] = name
        if notes is not UNSET:
            field_dict["notes"] = notes
        if player is not UNSET:
            field_dict["player"] = player
        if recipient_type is not UNSET:
            field_dict["recipientType"] = recipient_type
        if results is not UNSET:
            field_dict["results"] = results
        if season is not UNSET:
            field_dict["season"] = season
        if short_name is not UNSET:
            field_dict["shortName"] = short_name
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order
        if sport is not UNSET:
            field_dict["sport"] = sport
        if team is not UNSET:
            field_dict["team"] = team
        if votes is not UNSET:
            field_dict["votes"] = votes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_result_rest_object import AwardResultRestObject
        from ..models.baseball_person_rest_object import BaseballPersonRestObject
        from ..models.league_rest_object import LeagueRestObject
        from ..models.sport_rest_object import SportRestObject
        from ..models.team_rest_object import TeamRestObject

        d = dict(src_dict)
        _date = d.pop("date", UNSET)
        date: datetime.date | Unset
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        description = d.pop("description", UNSET)

        history = d.pop("history", UNSET)

        home_page_url = d.pop("homePageUrl", UNSET)

        id = d.pop("id", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        _league = d.pop("league", UNSET)
        league: LeagueRestObject | Unset
        if isinstance(_league, Unset):
            league = UNSET
        else:
            league = LeagueRestObject.from_dict(_league)

        name = d.pop("name", UNSET)

        notes = d.pop("notes", UNSET)

        _player = d.pop("player", UNSET)
        player: BaseballPersonRestObject | Unset
        if isinstance(_player, Unset):
            player = UNSET
        else:
            player = BaseballPersonRestObject.from_dict(_player)

        recipient_type = d.pop("recipientType", UNSET)

        _results = d.pop("results", UNSET)
        results: list[AwardResultRestObject] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = AwardResultRestObject.from_dict(results_item_data)

                results.append(results_item)

        season = d.pop("season", UNSET)

        short_name = d.pop("shortName", UNSET)

        sort_order = d.pop("sortOrder", UNSET)

        _sport = d.pop("sport", UNSET)
        sport: SportRestObject | Unset
        if isinstance(_sport, Unset):
            sport = UNSET
        else:
            sport = SportRestObject.from_dict(_sport)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        votes = d.pop("votes", UNSET)

        award_rest_object = cls(
            date=date,
            description=description,
            history=history,
            home_page_url=home_page_url,
            id=id,
            image_url=image_url,
            league=league,
            name=name,
            notes=notes,
            player=player,
            recipient_type=recipient_type,
            results=results,
            season=season,
            short_name=short_name,
            sort_order=sort_order,
            sport=sport,
            team=team,
            votes=votes,
        )

        award_rest_object.additional_properties = d
        return award_rest_object

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
