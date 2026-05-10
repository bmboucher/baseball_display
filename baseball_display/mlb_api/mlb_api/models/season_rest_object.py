from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeasonRestObject")


@_attrs_define
class SeasonRestObject:
    """
    Attributes:
        all_star_date (datetime.date | Unset): Date of the all-star game. Format: YYYY-MM-DD
        first_date_2_nd_half (datetime.date | Unset): Date of the first day of the second half of the regular season.
            Format: YYYY-MM-DD
        last_date_1_st_half (datetime.date | Unset): Date of the last day of the first half of the regular season.
            Format: YYYY-MM-DD
        post_season_end_date (datetime.date | Unset): Date the postseason ends. Format: YYYY-MM-DD
        post_season_start_date (datetime.date | Unset): Date the postseason starts. Format: YYYY-MM-DD
        pre_season_end_date (datetime.date | Unset): Date the preseason ends. Format: YYYY-MM-DD
        pre_season_start_date (datetime.date | Unset): Date the preseason starts. Format: YYYY-MM-DD
        regular_season_end_date (datetime.date | Unset): Date the regular season ends. Format: YYYY-MM-DD
        regular_season_start_date (datetime.date | Unset): Date the regular season starts. Format: YYYY-MM-DD
        season_id (str | Unset): Season of play
    """

    all_star_date: datetime.date | Unset = UNSET
    first_date_2_nd_half: datetime.date | Unset = UNSET
    last_date_1_st_half: datetime.date | Unset = UNSET
    post_season_end_date: datetime.date | Unset = UNSET
    post_season_start_date: datetime.date | Unset = UNSET
    pre_season_end_date: datetime.date | Unset = UNSET
    pre_season_start_date: datetime.date | Unset = UNSET
    regular_season_end_date: datetime.date | Unset = UNSET
    regular_season_start_date: datetime.date | Unset = UNSET
    season_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        all_star_date: str | Unset = UNSET
        if not isinstance(self.all_star_date, Unset):
            all_star_date = self.all_star_date.isoformat()

        first_date_2_nd_half: str | Unset = UNSET
        if not isinstance(self.first_date_2_nd_half, Unset):
            first_date_2_nd_half = self.first_date_2_nd_half.isoformat()

        last_date_1_st_half: str | Unset = UNSET
        if not isinstance(self.last_date_1_st_half, Unset):
            last_date_1_st_half = self.last_date_1_st_half.isoformat()

        post_season_end_date: str | Unset = UNSET
        if not isinstance(self.post_season_end_date, Unset):
            post_season_end_date = self.post_season_end_date.isoformat()

        post_season_start_date: str | Unset = UNSET
        if not isinstance(self.post_season_start_date, Unset):
            post_season_start_date = self.post_season_start_date.isoformat()

        pre_season_end_date: str | Unset = UNSET
        if not isinstance(self.pre_season_end_date, Unset):
            pre_season_end_date = self.pre_season_end_date.isoformat()

        pre_season_start_date: str | Unset = UNSET
        if not isinstance(self.pre_season_start_date, Unset):
            pre_season_start_date = self.pre_season_start_date.isoformat()

        regular_season_end_date: str | Unset = UNSET
        if not isinstance(self.regular_season_end_date, Unset):
            regular_season_end_date = self.regular_season_end_date.isoformat()

        regular_season_start_date: str | Unset = UNSET
        if not isinstance(self.regular_season_start_date, Unset):
            regular_season_start_date = self.regular_season_start_date.isoformat()

        season_id = self.season_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if all_star_date is not UNSET:
            field_dict["allStarDate"] = all_star_date
        if first_date_2_nd_half is not UNSET:
            field_dict["firstDate2ndHalf"] = first_date_2_nd_half
        if last_date_1_st_half is not UNSET:
            field_dict["lastDate1stHalf"] = last_date_1_st_half
        if post_season_end_date is not UNSET:
            field_dict["postSeasonEndDate"] = post_season_end_date
        if post_season_start_date is not UNSET:
            field_dict["postSeasonStartDate"] = post_season_start_date
        if pre_season_end_date is not UNSET:
            field_dict["preSeasonEndDate"] = pre_season_end_date
        if pre_season_start_date is not UNSET:
            field_dict["preSeasonStartDate"] = pre_season_start_date
        if regular_season_end_date is not UNSET:
            field_dict["regularSeasonEndDate"] = regular_season_end_date
        if regular_season_start_date is not UNSET:
            field_dict["regularSeasonStartDate"] = regular_season_start_date
        if season_id is not UNSET:
            field_dict["seasonId"] = season_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _all_star_date = d.pop("allStarDate", UNSET)
        all_star_date: datetime.date | Unset
        if isinstance(_all_star_date, Unset):
            all_star_date = UNSET
        else:
            all_star_date = isoparse(_all_star_date).date()

        _first_date_2_nd_half = d.pop("firstDate2ndHalf", UNSET)
        first_date_2_nd_half: datetime.date | Unset
        if isinstance(_first_date_2_nd_half, Unset):
            first_date_2_nd_half = UNSET
        else:
            first_date_2_nd_half = isoparse(_first_date_2_nd_half).date()

        _last_date_1_st_half = d.pop("lastDate1stHalf", UNSET)
        last_date_1_st_half: datetime.date | Unset
        if isinstance(_last_date_1_st_half, Unset):
            last_date_1_st_half = UNSET
        else:
            last_date_1_st_half = isoparse(_last_date_1_st_half).date()

        _post_season_end_date = d.pop("postSeasonEndDate", UNSET)
        post_season_end_date: datetime.date | Unset
        if isinstance(_post_season_end_date, Unset):
            post_season_end_date = UNSET
        else:
            post_season_end_date = isoparse(_post_season_end_date).date()

        _post_season_start_date = d.pop("postSeasonStartDate", UNSET)
        post_season_start_date: datetime.date | Unset
        if isinstance(_post_season_start_date, Unset):
            post_season_start_date = UNSET
        else:
            post_season_start_date = isoparse(_post_season_start_date).date()

        _pre_season_end_date = d.pop("preSeasonEndDate", UNSET)
        pre_season_end_date: datetime.date | Unset
        if isinstance(_pre_season_end_date, Unset):
            pre_season_end_date = UNSET
        else:
            pre_season_end_date = isoparse(_pre_season_end_date).date()

        _pre_season_start_date = d.pop("preSeasonStartDate", UNSET)
        pre_season_start_date: datetime.date | Unset
        if isinstance(_pre_season_start_date, Unset):
            pre_season_start_date = UNSET
        else:
            pre_season_start_date = isoparse(_pre_season_start_date).date()

        _regular_season_end_date = d.pop("regularSeasonEndDate", UNSET)
        regular_season_end_date: datetime.date | Unset
        if isinstance(_regular_season_end_date, Unset):
            regular_season_end_date = UNSET
        else:
            regular_season_end_date = isoparse(_regular_season_end_date).date()

        _regular_season_start_date = d.pop("regularSeasonStartDate", UNSET)
        regular_season_start_date: datetime.date | Unset
        if isinstance(_regular_season_start_date, Unset):
            regular_season_start_date = UNSET
        else:
            regular_season_start_date = isoparse(_regular_season_start_date).date()

        season_id = d.pop("seasonId", UNSET)

        season_rest_object = cls(
            all_star_date=all_star_date,
            first_date_2_nd_half=first_date_2_nd_half,
            last_date_1_st_half=last_date_1_st_half,
            post_season_end_date=post_season_end_date,
            post_season_start_date=post_season_start_date,
            pre_season_end_date=pre_season_end_date,
            pre_season_start_date=pre_season_start_date,
            regular_season_end_date=regular_season_end_date,
            regular_season_start_date=regular_season_start_date,
            season_id=season_id,
        )

        season_rest_object.additional_properties = d
        return season_rest_object

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
