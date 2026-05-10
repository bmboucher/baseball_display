from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.streak_rest_object import StreakRestObject
    from ..models.team_rest_object import TeamRestObject
    from ..models.win_loss_record_rest_object import WinLossRecordRestObject


T = TypeVar("T", bound="TeamStandingsRecordRestObject")


@_attrs_define
class TeamStandingsRecordRestObject:
    """
    Attributes:
        clinch_indicator (str | Unset):
        conference (Any | Unset):
        conference_games_back (str | Unset):
        conference_rank (str | Unset):
        division (Any | Unset):
        division_games_back (str | Unset):
        division_rank (str | Unset):
        games_back (str | Unset):
        games_played (int | Unset):
        league (Any | Unset):
        league_games_back (str | Unset):
        league_rank (str | Unset):
        league_record (WinLossRecordRestObject | Unset):
        season (str | Unset):
        sport_games_back (str | Unset):
        sport_rank (str | Unset):
        spring_league_games_back (str | Unset):
        spring_league_rank (str | Unset):
        streak (StreakRestObject | Unset):
        team (TeamRestObject | Unset):
        wild_card_games_back (str | Unset):
        wild_card_rank (str | Unset):
    """

    clinch_indicator: str | Unset = UNSET
    conference: Any | Unset = UNSET
    conference_games_back: str | Unset = UNSET
    conference_rank: str | Unset = UNSET
    division: Any | Unset = UNSET
    division_games_back: str | Unset = UNSET
    division_rank: str | Unset = UNSET
    games_back: str | Unset = UNSET
    games_played: int | Unset = UNSET
    league: Any | Unset = UNSET
    league_games_back: str | Unset = UNSET
    league_rank: str | Unset = UNSET
    league_record: WinLossRecordRestObject | Unset = UNSET
    season: str | Unset = UNSET
    sport_games_back: str | Unset = UNSET
    sport_rank: str | Unset = UNSET
    spring_league_games_back: str | Unset = UNSET
    spring_league_rank: str | Unset = UNSET
    streak: StreakRestObject | Unset = UNSET
    team: TeamRestObject | Unset = UNSET
    wild_card_games_back: str | Unset = UNSET
    wild_card_rank: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.streak_rest_object import StreakRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.win_loss_record_rest_object import WinLossRecordRestObject

        clinch_indicator = self.clinch_indicator

        conference = self.conference

        conference_games_back = self.conference_games_back

        conference_rank = self.conference_rank

        division = self.division

        division_games_back = self.division_games_back

        division_rank = self.division_rank

        games_back = self.games_back

        games_played = self.games_played

        league = self.league

        league_games_back = self.league_games_back

        league_rank = self.league_rank

        league_record: dict[str, Any] | Unset = UNSET
        if not isinstance(self.league_record, Unset):
            league_record = self.league_record.to_dict()

        season = self.season

        sport_games_back = self.sport_games_back

        sport_rank = self.sport_rank

        spring_league_games_back = self.spring_league_games_back

        spring_league_rank = self.spring_league_rank

        streak: dict[str, Any] | Unset = UNSET
        if not isinstance(self.streak, Unset):
            streak = self.streak.to_dict()

        team: dict[str, Any] | Unset = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        wild_card_games_back = self.wild_card_games_back

        wild_card_rank = self.wild_card_rank

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clinch_indicator is not UNSET:
            field_dict["clinchIndicator"] = clinch_indicator
        if conference is not UNSET:
            field_dict["conference"] = conference
        if conference_games_back is not UNSET:
            field_dict["conferenceGamesBack"] = conference_games_back
        if conference_rank is not UNSET:
            field_dict["conferenceRank"] = conference_rank
        if division is not UNSET:
            field_dict["division"] = division
        if division_games_back is not UNSET:
            field_dict["divisionGamesBack"] = division_games_back
        if division_rank is not UNSET:
            field_dict["divisionRank"] = division_rank
        if games_back is not UNSET:
            field_dict["gamesBack"] = games_back
        if games_played is not UNSET:
            field_dict["gamesPlayed"] = games_played
        if league is not UNSET:
            field_dict["league"] = league
        if league_games_back is not UNSET:
            field_dict["leagueGamesBack"] = league_games_back
        if league_rank is not UNSET:
            field_dict["leagueRank"] = league_rank
        if league_record is not UNSET:
            field_dict["leagueRecord"] = league_record
        if season is not UNSET:
            field_dict["season"] = season
        if sport_games_back is not UNSET:
            field_dict["sportGamesBack"] = sport_games_back
        if sport_rank is not UNSET:
            field_dict["sportRank"] = sport_rank
        if spring_league_games_back is not UNSET:
            field_dict["springLeagueGamesBack"] = spring_league_games_back
        if spring_league_rank is not UNSET:
            field_dict["springLeagueRank"] = spring_league_rank
        if streak is not UNSET:
            field_dict["streak"] = streak
        if team is not UNSET:
            field_dict["team"] = team
        if wild_card_games_back is not UNSET:
            field_dict["wildCardGamesBack"] = wild_card_games_back
        if wild_card_rank is not UNSET:
            field_dict["wildCardRank"] = wild_card_rank

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.streak_rest_object import StreakRestObject
        from ..models.team_rest_object import TeamRestObject
        from ..models.win_loss_record_rest_object import WinLossRecordRestObject

        d = dict(src_dict)
        clinch_indicator = d.pop("clinchIndicator", UNSET)

        conference = d.pop("conference", UNSET)

        conference_games_back = d.pop("conferenceGamesBack", UNSET)

        conference_rank = d.pop("conferenceRank", UNSET)

        division = d.pop("division", UNSET)

        division_games_back = d.pop("divisionGamesBack", UNSET)

        division_rank = d.pop("divisionRank", UNSET)

        games_back = d.pop("gamesBack", UNSET)

        games_played = d.pop("gamesPlayed", UNSET)

        league = d.pop("league", UNSET)

        league_games_back = d.pop("leagueGamesBack", UNSET)

        league_rank = d.pop("leagueRank", UNSET)

        _league_record = d.pop("leagueRecord", UNSET)
        league_record: WinLossRecordRestObject | Unset
        if isinstance(_league_record, Unset):
            league_record = UNSET
        else:
            league_record = WinLossRecordRestObject.from_dict(_league_record)

        season = d.pop("season", UNSET)

        sport_games_back = d.pop("sportGamesBack", UNSET)

        sport_rank = d.pop("sportRank", UNSET)

        spring_league_games_back = d.pop("springLeagueGamesBack", UNSET)

        spring_league_rank = d.pop("springLeagueRank", UNSET)

        _streak = d.pop("streak", UNSET)
        streak: StreakRestObject | Unset
        if isinstance(_streak, Unset):
            streak = UNSET
        else:
            streak = StreakRestObject.from_dict(_streak)

        _team = d.pop("team", UNSET)
        team: TeamRestObject | Unset
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = TeamRestObject.from_dict(_team)

        wild_card_games_back = d.pop("wildCardGamesBack", UNSET)

        wild_card_rank = d.pop("wildCardRank", UNSET)

        team_standings_record_rest_object = cls(
            clinch_indicator=clinch_indicator,
            conference=conference,
            conference_games_back=conference_games_back,
            conference_rank=conference_rank,
            division=division,
            division_games_back=division_games_back,
            division_rank=division_rank,
            games_back=games_back,
            games_played=games_played,
            league=league,
            league_games_back=league_games_back,
            league_rank=league_rank,
            league_record=league_record,
            season=season,
            sport_games_back=sport_games_back,
            sport_rank=sport_rank,
            spring_league_games_back=spring_league_games_back,
            spring_league_rank=spring_league_rank,
            streak=streak,
            team=team,
            wild_card_games_back=wild_card_games_back,
            wild_card_rank=wild_card_rank,
        )

        team_standings_record_rest_object.additional_properties = d
        return team_standings_record_rest_object

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
