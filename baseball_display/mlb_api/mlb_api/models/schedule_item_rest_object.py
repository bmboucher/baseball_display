from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.broadcast_rest_object import BroadcastRestObject
    from ..models.decision_rest_object import DecisionRestObject
    from ..models.game_content_rest_object import GameContentRestObject
    from ..models.game_info_rest_object import GameInfoRestObject
    from ..models.game_status_rest_object import GameStatusRestObject
    from ..models.official_rest_object import OfficialRestObject
    from ..models.play_rest_object import PlayRestObject
    from ..models.promotion_rest_object import PromotionRestObject
    from ..models.series_status_rest_object import SeriesStatusRestObject
    from ..models.ticket_rest_object import TicketRestObject
    from ..models.venue_rest_object import VenueRestObject
    from ..models.weather_rest_object import WeatherRestObject


T = TypeVar("T", bound="ScheduleItemRestObject")


@_attrs_define
class ScheduleItemRestObject:
    """
    Attributes:
        at_bat_promotions (list[PromotionRestObject] | Unset): All of the promotional details
        at_bat_tickets (list[TicketRestObject] | Unset): All of the ticket details
        broadcasts (list[BroadcastRestObject] | Unset): All of the broadcast details
        content (GameContentRestObject | Unset):
        decisions (DecisionRestObject | Unset):
        end_date_time (datetime.datetime | Unset): Format: YYYY-MM-DDTHH:MM:SSZ
        game_date (datetime.datetime | Unset): Date of Game. Format: MM/DD/YYYY
        game_info (GameInfoRestObject | Unset):
        game_number (int | Unset):
        game_pk (int | Unset): Unique Primary Key Representing a Game
        game_type (str | Unset): Type of Game. Available types in /api/v1/gameTypes
        is_default_game (bool | Unset):
        is_featured_game (bool | Unset):
        is_tie (bool | Unset):
        link (str | Unset): Link to full resource
        officials (list[OfficialRestObject] | Unset):
        promotions (list[PromotionRestObject] | Unset): All of the promotional details
        public_facing (bool | Unset):
        radio_broadcasts (list[BroadcastRestObject] | Unset): All of the radio broadcast details
        reschedule_date (datetime.datetime | Unset):
        rescheduled_from (datetime.datetime | Unset):
        resume_date (datetime.datetime | Unset):
        resumed_from (datetime.datetime | Unset):
        scoring_plays (list[PlayRestObject] | Unset):
        season (str | Unset): Season of play
        series_status (SeriesStatusRestObject | Unset):
        series_summary (Any | Unset):
        sort_number (int | Unset):
        sponsorships (list[PromotionRestObject] | Unset): All of the sponsorship details
        status (GameStatusRestObject | Unset):
        tickets (list[TicketRestObject] | Unset): All of the ticket details
        venue (VenueRestObject | Unset):
        weather (WeatherRestObject | Unset):
        xref_ids (list[Any] | Unset):
    """

    at_bat_promotions: list[PromotionRestObject] | Unset = UNSET
    at_bat_tickets: list[TicketRestObject] | Unset = UNSET
    broadcasts: list[BroadcastRestObject] | Unset = UNSET
    content: GameContentRestObject | Unset = UNSET
    decisions: DecisionRestObject | Unset = UNSET
    end_date_time: datetime.datetime | Unset = UNSET
    game_date: datetime.datetime | Unset = UNSET
    game_info: GameInfoRestObject | Unset = UNSET
    game_number: int | Unset = UNSET
    game_pk: int | Unset = UNSET
    game_type: str | Unset = UNSET
    is_default_game: bool | Unset = UNSET
    is_featured_game: bool | Unset = UNSET
    is_tie: bool | Unset = UNSET
    link: str | Unset = UNSET
    officials: list[OfficialRestObject] | Unset = UNSET
    promotions: list[PromotionRestObject] | Unset = UNSET
    public_facing: bool | Unset = UNSET
    radio_broadcasts: list[BroadcastRestObject] | Unset = UNSET
    reschedule_date: datetime.datetime | Unset = UNSET
    rescheduled_from: datetime.datetime | Unset = UNSET
    resume_date: datetime.datetime | Unset = UNSET
    resumed_from: datetime.datetime | Unset = UNSET
    scoring_plays: list[PlayRestObject] | Unset = UNSET
    season: str | Unset = UNSET
    series_status: SeriesStatusRestObject | Unset = UNSET
    series_summary: Any | Unset = UNSET
    sort_number: int | Unset = UNSET
    sponsorships: list[PromotionRestObject] | Unset = UNSET
    status: GameStatusRestObject | Unset = UNSET
    tickets: list[TicketRestObject] | Unset = UNSET
    venue: VenueRestObject | Unset = UNSET
    weather: WeatherRestObject | Unset = UNSET
    xref_ids: list[Any] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.broadcast_rest_object import BroadcastRestObject
        from ..models.decision_rest_object import DecisionRestObject
        from ..models.game_content_rest_object import GameContentRestObject
        from ..models.game_info_rest_object import GameInfoRestObject
        from ..models.game_status_rest_object import GameStatusRestObject
        from ..models.official_rest_object import OfficialRestObject
        from ..models.play_rest_object import PlayRestObject
        from ..models.promotion_rest_object import PromotionRestObject
        from ..models.series_status_rest_object import SeriesStatusRestObject
        from ..models.ticket_rest_object import TicketRestObject
        from ..models.venue_rest_object import VenueRestObject
        from ..models.weather_rest_object import WeatherRestObject

        at_bat_promotions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.at_bat_promotions, Unset):
            at_bat_promotions = []
            for at_bat_promotions_item_data in self.at_bat_promotions:
                at_bat_promotions_item = at_bat_promotions_item_data.to_dict()
                at_bat_promotions.append(at_bat_promotions_item)

        at_bat_tickets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.at_bat_tickets, Unset):
            at_bat_tickets = []
            for at_bat_tickets_item_data in self.at_bat_tickets:
                at_bat_tickets_item = at_bat_tickets_item_data.to_dict()
                at_bat_tickets.append(at_bat_tickets_item)

        broadcasts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.broadcasts, Unset):
            broadcasts = []
            for broadcasts_item_data in self.broadcasts:
                broadcasts_item = broadcasts_item_data.to_dict()
                broadcasts.append(broadcasts_item)

        content: dict[str, Any] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_dict()

        decisions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decisions, Unset):
            decisions = self.decisions.to_dict()

        end_date_time: str | Unset = UNSET
        if not isinstance(self.end_date_time, Unset):
            end_date_time = self.end_date_time.isoformat()

        game_date: str | Unset = UNSET
        if not isinstance(self.game_date, Unset):
            game_date = self.game_date.isoformat()

        game_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.game_info, Unset):
            game_info = self.game_info.to_dict()

        game_number = self.game_number

        game_pk = self.game_pk

        game_type = self.game_type

        is_default_game = self.is_default_game

        is_featured_game = self.is_featured_game

        is_tie = self.is_tie

        link = self.link

        officials: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.officials, Unset):
            officials = []
            for officials_item_data in self.officials:
                officials_item = officials_item_data.to_dict()
                officials.append(officials_item)

        promotions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.promotions, Unset):
            promotions = []
            for promotions_item_data in self.promotions:
                promotions_item = promotions_item_data.to_dict()
                promotions.append(promotions_item)

        public_facing = self.public_facing

        radio_broadcasts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.radio_broadcasts, Unset):
            radio_broadcasts = []
            for radio_broadcasts_item_data in self.radio_broadcasts:
                radio_broadcasts_item = radio_broadcasts_item_data.to_dict()
                radio_broadcasts.append(radio_broadcasts_item)

        reschedule_date: str | Unset = UNSET
        if not isinstance(self.reschedule_date, Unset):
            reschedule_date = self.reschedule_date.isoformat()

        rescheduled_from: str | Unset = UNSET
        if not isinstance(self.rescheduled_from, Unset):
            rescheduled_from = self.rescheduled_from.isoformat()

        resume_date: str | Unset = UNSET
        if not isinstance(self.resume_date, Unset):
            resume_date = self.resume_date.isoformat()

        resumed_from: str | Unset = UNSET
        if not isinstance(self.resumed_from, Unset):
            resumed_from = self.resumed_from.isoformat()

        scoring_plays: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.scoring_plays, Unset):
            scoring_plays = []
            for scoring_plays_item_data in self.scoring_plays:
                scoring_plays_item = scoring_plays_item_data.to_dict()
                scoring_plays.append(scoring_plays_item)

        season = self.season

        series_status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.series_status, Unset):
            series_status = self.series_status.to_dict()

        series_summary = self.series_summary

        sort_number = self.sort_number

        sponsorships: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sponsorships, Unset):
            sponsorships = []
            for sponsorships_item_data in self.sponsorships:
                sponsorships_item = sponsorships_item_data.to_dict()
                sponsorships.append(sponsorships_item)

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        tickets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tickets, Unset):
            tickets = []
            for tickets_item_data in self.tickets:
                tickets_item = tickets_item_data.to_dict()
                tickets.append(tickets_item)

        venue: dict[str, Any] | Unset = UNSET
        if not isinstance(self.venue, Unset):
            venue = self.venue.to_dict()

        weather: dict[str, Any] | Unset = UNSET
        if not isinstance(self.weather, Unset):
            weather = self.weather.to_dict()

        xref_ids: list[Any] | Unset = UNSET
        if not isinstance(self.xref_ids, Unset):
            xref_ids = self.xref_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at_bat_promotions is not UNSET:
            field_dict["atBatPromotions"] = at_bat_promotions
        if at_bat_tickets is not UNSET:
            field_dict["atBatTickets"] = at_bat_tickets
        if broadcasts is not UNSET:
            field_dict["broadcasts"] = broadcasts
        if content is not UNSET:
            field_dict["content"] = content
        if decisions is not UNSET:
            field_dict["decisions"] = decisions
        if end_date_time is not UNSET:
            field_dict["endDateTime"] = end_date_time
        if game_date is not UNSET:
            field_dict["gameDate"] = game_date
        if game_info is not UNSET:
            field_dict["gameInfo"] = game_info
        if game_number is not UNSET:
            field_dict["gameNumber"] = game_number
        if game_pk is not UNSET:
            field_dict["gamePk"] = game_pk
        if game_type is not UNSET:
            field_dict["gameType"] = game_type
        if is_default_game is not UNSET:
            field_dict["isDefaultGame"] = is_default_game
        if is_featured_game is not UNSET:
            field_dict["isFeaturedGame"] = is_featured_game
        if is_tie is not UNSET:
            field_dict["isTie"] = is_tie
        if link is not UNSET:
            field_dict["link"] = link
        if officials is not UNSET:
            field_dict["officials"] = officials
        if promotions is not UNSET:
            field_dict["promotions"] = promotions
        if public_facing is not UNSET:
            field_dict["publicFacing"] = public_facing
        if radio_broadcasts is not UNSET:
            field_dict["radioBroadcasts"] = radio_broadcasts
        if reschedule_date is not UNSET:
            field_dict["rescheduleDate"] = reschedule_date
        if rescheduled_from is not UNSET:
            field_dict["rescheduledFrom"] = rescheduled_from
        if resume_date is not UNSET:
            field_dict["resumeDate"] = resume_date
        if resumed_from is not UNSET:
            field_dict["resumedFrom"] = resumed_from
        if scoring_plays is not UNSET:
            field_dict["scoringPlays"] = scoring_plays
        if season is not UNSET:
            field_dict["season"] = season
        if series_status is not UNSET:
            field_dict["seriesStatus"] = series_status
        if series_summary is not UNSET:
            field_dict["seriesSummary"] = series_summary
        if sort_number is not UNSET:
            field_dict["sortNumber"] = sort_number
        if sponsorships is not UNSET:
            field_dict["sponsorships"] = sponsorships
        if status is not UNSET:
            field_dict["status"] = status
        if tickets is not UNSET:
            field_dict["tickets"] = tickets
        if venue is not UNSET:
            field_dict["venue"] = venue
        if weather is not UNSET:
            field_dict["weather"] = weather
        if xref_ids is not UNSET:
            field_dict["xrefIds"] = xref_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.broadcast_rest_object import BroadcastRestObject
        from ..models.decision_rest_object import DecisionRestObject
        from ..models.game_content_rest_object import GameContentRestObject
        from ..models.game_info_rest_object import GameInfoRestObject
        from ..models.game_status_rest_object import GameStatusRestObject
        from ..models.official_rest_object import OfficialRestObject
        from ..models.play_rest_object import PlayRestObject
        from ..models.promotion_rest_object import PromotionRestObject
        from ..models.series_status_rest_object import SeriesStatusRestObject
        from ..models.ticket_rest_object import TicketRestObject
        from ..models.venue_rest_object import VenueRestObject
        from ..models.weather_rest_object import WeatherRestObject

        d = dict(src_dict)
        _at_bat_promotions = d.pop("atBatPromotions", UNSET)
        at_bat_promotions: list[PromotionRestObject] | Unset = UNSET
        if _at_bat_promotions is not UNSET:
            at_bat_promotions = []
            for at_bat_promotions_item_data in _at_bat_promotions:
                at_bat_promotions_item = PromotionRestObject.from_dict(
                    at_bat_promotions_item_data
                )

                at_bat_promotions.append(at_bat_promotions_item)

        _at_bat_tickets = d.pop("atBatTickets", UNSET)
        at_bat_tickets: list[TicketRestObject] | Unset = UNSET
        if _at_bat_tickets is not UNSET:
            at_bat_tickets = []
            for at_bat_tickets_item_data in _at_bat_tickets:
                at_bat_tickets_item = TicketRestObject.from_dict(
                    at_bat_tickets_item_data
                )

                at_bat_tickets.append(at_bat_tickets_item)

        _broadcasts = d.pop("broadcasts", UNSET)
        broadcasts: list[BroadcastRestObject] | Unset = UNSET
        if _broadcasts is not UNSET:
            broadcasts = []
            for broadcasts_item_data in _broadcasts:
                broadcasts_item = BroadcastRestObject.from_dict(broadcasts_item_data)

                broadcasts.append(broadcasts_item)

        _content = d.pop("content", UNSET)
        content: GameContentRestObject | Unset
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = GameContentRestObject.from_dict(_content)

        _decisions = d.pop("decisions", UNSET)
        decisions: DecisionRestObject | Unset
        if isinstance(_decisions, Unset):
            decisions = UNSET
        else:
            decisions = DecisionRestObject.from_dict(_decisions)

        _end_date_time = d.pop("endDateTime", UNSET)
        end_date_time: datetime.datetime | Unset
        if isinstance(_end_date_time, Unset):
            end_date_time = UNSET
        else:
            end_date_time = isoparse(_end_date_time)

        _game_date = d.pop("gameDate", UNSET)
        game_date: datetime.datetime | Unset
        if isinstance(_game_date, Unset):
            game_date = UNSET
        else:
            game_date = isoparse(_game_date)

        _game_info = d.pop("gameInfo", UNSET)
        game_info: GameInfoRestObject | Unset
        if isinstance(_game_info, Unset):
            game_info = UNSET
        else:
            game_info = GameInfoRestObject.from_dict(_game_info)

        game_number = d.pop("gameNumber", UNSET)

        game_pk = d.pop("gamePk", UNSET)

        game_type = d.pop("gameType", UNSET)

        is_default_game = d.pop("isDefaultGame", UNSET)

        is_featured_game = d.pop("isFeaturedGame", UNSET)

        is_tie = d.pop("isTie", UNSET)

        link = d.pop("link", UNSET)

        _officials = d.pop("officials", UNSET)
        officials: list[OfficialRestObject] | Unset = UNSET
        if _officials is not UNSET:
            officials = []
            for officials_item_data in _officials:
                officials_item = OfficialRestObject.from_dict(officials_item_data)

                officials.append(officials_item)

        _promotions = d.pop("promotions", UNSET)
        promotions: list[PromotionRestObject] | Unset = UNSET
        if _promotions is not UNSET:
            promotions = []
            for promotions_item_data in _promotions:
                promotions_item = PromotionRestObject.from_dict(promotions_item_data)

                promotions.append(promotions_item)

        public_facing = d.pop("publicFacing", UNSET)

        _radio_broadcasts = d.pop("radioBroadcasts", UNSET)
        radio_broadcasts: list[BroadcastRestObject] | Unset = UNSET
        if _radio_broadcasts is not UNSET:
            radio_broadcasts = []
            for radio_broadcasts_item_data in _radio_broadcasts:
                radio_broadcasts_item = BroadcastRestObject.from_dict(
                    radio_broadcasts_item_data
                )

                radio_broadcasts.append(radio_broadcasts_item)

        _reschedule_date = d.pop("rescheduleDate", UNSET)
        reschedule_date: datetime.datetime | Unset
        if isinstance(_reschedule_date, Unset):
            reschedule_date = UNSET
        else:
            reschedule_date = isoparse(_reschedule_date)

        _rescheduled_from = d.pop("rescheduledFrom", UNSET)
        rescheduled_from: datetime.datetime | Unset
        if isinstance(_rescheduled_from, Unset):
            rescheduled_from = UNSET
        else:
            rescheduled_from = isoparse(_rescheduled_from)

        _resume_date = d.pop("resumeDate", UNSET)
        resume_date: datetime.datetime | Unset
        if isinstance(_resume_date, Unset):
            resume_date = UNSET
        else:
            resume_date = isoparse(_resume_date)

        _resumed_from = d.pop("resumedFrom", UNSET)
        resumed_from: datetime.datetime | Unset
        if isinstance(_resumed_from, Unset):
            resumed_from = UNSET
        else:
            resumed_from = isoparse(_resumed_from)

        _scoring_plays = d.pop("scoringPlays", UNSET)
        scoring_plays: list[PlayRestObject] | Unset = UNSET
        if _scoring_plays is not UNSET:
            scoring_plays = []
            for scoring_plays_item_data in _scoring_plays:
                scoring_plays_item = PlayRestObject.from_dict(scoring_plays_item_data)

                scoring_plays.append(scoring_plays_item)

        season = d.pop("season", UNSET)

        _series_status = d.pop("seriesStatus", UNSET)
        series_status: SeriesStatusRestObject | Unset
        if isinstance(_series_status, Unset):
            series_status = UNSET
        else:
            series_status = SeriesStatusRestObject.from_dict(_series_status)

        series_summary = d.pop("seriesSummary", UNSET)

        sort_number = d.pop("sortNumber", UNSET)

        _sponsorships = d.pop("sponsorships", UNSET)
        sponsorships: list[PromotionRestObject] | Unset = UNSET
        if _sponsorships is not UNSET:
            sponsorships = []
            for sponsorships_item_data in _sponsorships:
                sponsorships_item = PromotionRestObject.from_dict(
                    sponsorships_item_data
                )

                sponsorships.append(sponsorships_item)

        _status = d.pop("status", UNSET)
        status: GameStatusRestObject | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GameStatusRestObject.from_dict(_status)

        _tickets = d.pop("tickets", UNSET)
        tickets: list[TicketRestObject] | Unset = UNSET
        if _tickets is not UNSET:
            tickets = []
            for tickets_item_data in _tickets:
                tickets_item = TicketRestObject.from_dict(tickets_item_data)

                tickets.append(tickets_item)

        _venue = d.pop("venue", UNSET)
        venue: VenueRestObject | Unset
        if isinstance(_venue, Unset):
            venue = UNSET
        else:
            venue = VenueRestObject.from_dict(_venue)

        _weather = d.pop("weather", UNSET)
        weather: WeatherRestObject | Unset
        if isinstance(_weather, Unset):
            weather = UNSET
        else:
            weather = WeatherRestObject.from_dict(_weather)

        xref_ids = cast(list[Any], d.pop("xrefIds", UNSET))

        schedule_item_rest_object = cls(
            at_bat_promotions=at_bat_promotions,
            at_bat_tickets=at_bat_tickets,
            broadcasts=broadcasts,
            content=content,
            decisions=decisions,
            end_date_time=end_date_time,
            game_date=game_date,
            game_info=game_info,
            game_number=game_number,
            game_pk=game_pk,
            game_type=game_type,
            is_default_game=is_default_game,
            is_featured_game=is_featured_game,
            is_tie=is_tie,
            link=link,
            officials=officials,
            promotions=promotions,
            public_facing=public_facing,
            radio_broadcasts=radio_broadcasts,
            reschedule_date=reschedule_date,
            rescheduled_from=rescheduled_from,
            resume_date=resume_date,
            resumed_from=resumed_from,
            scoring_plays=scoring_plays,
            season=season,
            series_status=series_status,
            series_summary=series_summary,
            sort_number=sort_number,
            sponsorships=sponsorships,
            status=status,
            tickets=tickets,
            venue=venue,
            weather=weather,
            xref_ids=xref_ids,
        )

        schedule_item_rest_object.additional_properties = d
        return schedule_item_rest_object

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
