from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
    from ..models.transaction_rest_object import TransactionRestObject


T = TypeVar("T", bound="BaseballPersonRestObject")


@_attrs_define
class BaseballPersonRestObject:
    """
    Attributes:
        articles (list[Any] | Unset):
        bat_side (DynamicEnumRestObject | Unset):
        drafts (list[Any] | Unset):
        first_last_name (str | Unset):
        full_fml_name (str | Unset):
        full_lfm_name (str | Unset):
        init_last_name (str | Unset):
        last_first_name (str | Unset):
        last_init_name (str | Unset):
        mixed_feed (list[Any] | Unset):
        mlb_debut_date (datetime.date | Unset):
        name_slug (str | Unset):
        name_title (str | Unset):
        note (str | Unset):
        pitch_hand (DynamicEnumRestObject | Unset):
        strike_zone_bottom (float | Unset):
        strike_zone_top (float | Unset):
        transactions (list[TransactionRestObject] | Unset):
        videos (list[Any] | Unset):
    """

    articles: list[Any] | Unset = UNSET
    bat_side: DynamicEnumRestObject | Unset = UNSET
    drafts: list[Any] | Unset = UNSET
    first_last_name: str | Unset = UNSET
    full_fml_name: str | Unset = UNSET
    full_lfm_name: str | Unset = UNSET
    init_last_name: str | Unset = UNSET
    last_first_name: str | Unset = UNSET
    last_init_name: str | Unset = UNSET
    mixed_feed: list[Any] | Unset = UNSET
    mlb_debut_date: datetime.date | Unset = UNSET
    name_slug: str | Unset = UNSET
    name_title: str | Unset = UNSET
    note: str | Unset = UNSET
    pitch_hand: DynamicEnumRestObject | Unset = UNSET
    strike_zone_bottom: float | Unset = UNSET
    strike_zone_top: float | Unset = UNSET
    transactions: list[TransactionRestObject] | Unset = UNSET
    videos: list[Any] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
        from ..models.transaction_rest_object import TransactionRestObject

        articles: list[Any] | Unset = UNSET
        if not isinstance(self.articles, Unset):
            articles = self.articles

        bat_side: dict[str, Any] | Unset = UNSET
        if not isinstance(self.bat_side, Unset):
            bat_side = self.bat_side.to_dict()

        drafts: list[Any] | Unset = UNSET
        if not isinstance(self.drafts, Unset):
            drafts = self.drafts

        first_last_name = self.first_last_name

        full_fml_name = self.full_fml_name

        full_lfm_name = self.full_lfm_name

        init_last_name = self.init_last_name

        last_first_name = self.last_first_name

        last_init_name = self.last_init_name

        mixed_feed: list[Any] | Unset = UNSET
        if not isinstance(self.mixed_feed, Unset):
            mixed_feed = self.mixed_feed

        mlb_debut_date: str | Unset = UNSET
        if not isinstance(self.mlb_debut_date, Unset):
            mlb_debut_date = self.mlb_debut_date.isoformat()

        name_slug = self.name_slug

        name_title = self.name_title

        note = self.note

        pitch_hand: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pitch_hand, Unset):
            pitch_hand = self.pitch_hand.to_dict()

        strike_zone_bottom = self.strike_zone_bottom

        strike_zone_top = self.strike_zone_top

        transactions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        videos: list[Any] | Unset = UNSET
        if not isinstance(self.videos, Unset):
            videos = self.videos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if articles is not UNSET:
            field_dict["articles"] = articles
        if bat_side is not UNSET:
            field_dict["batSide"] = bat_side
        if drafts is not UNSET:
            field_dict["drafts"] = drafts
        if first_last_name is not UNSET:
            field_dict["firstLastName"] = first_last_name
        if full_fml_name is not UNSET:
            field_dict["fullFMLName"] = full_fml_name
        if full_lfm_name is not UNSET:
            field_dict["fullLFMName"] = full_lfm_name
        if init_last_name is not UNSET:
            field_dict["initLastName"] = init_last_name
        if last_first_name is not UNSET:
            field_dict["lastFirstName"] = last_first_name
        if last_init_name is not UNSET:
            field_dict["lastInitName"] = last_init_name
        if mixed_feed is not UNSET:
            field_dict["mixedFeed"] = mixed_feed
        if mlb_debut_date is not UNSET:
            field_dict["mlbDebutDate"] = mlb_debut_date
        if name_slug is not UNSET:
            field_dict["nameSlug"] = name_slug
        if name_title is not UNSET:
            field_dict["nameTitle"] = name_title
        if note is not UNSET:
            field_dict["note"] = note
        if pitch_hand is not UNSET:
            field_dict["pitchHand"] = pitch_hand
        if strike_zone_bottom is not UNSET:
            field_dict["strikeZoneBottom"] = strike_zone_bottom
        if strike_zone_top is not UNSET:
            field_dict["strikeZoneTop"] = strike_zone_top
        if transactions is not UNSET:
            field_dict["transactions"] = transactions
        if videos is not UNSET:
            field_dict["videos"] = videos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dynamic_enum_rest_object import DynamicEnumRestObject
        from ..models.transaction_rest_object import TransactionRestObject

        d = dict(src_dict)
        articles = cast(list[Any], d.pop("articles", UNSET))

        _bat_side = d.pop("batSide", UNSET)
        bat_side: DynamicEnumRestObject | Unset
        if isinstance(_bat_side, Unset):
            bat_side = UNSET
        else:
            bat_side = DynamicEnumRestObject.from_dict(_bat_side)

        drafts = cast(list[Any], d.pop("drafts", UNSET))

        first_last_name = d.pop("firstLastName", UNSET)

        full_fml_name = d.pop("fullFMLName", UNSET)

        full_lfm_name = d.pop("fullLFMName", UNSET)

        init_last_name = d.pop("initLastName", UNSET)

        last_first_name = d.pop("lastFirstName", UNSET)

        last_init_name = d.pop("lastInitName", UNSET)

        mixed_feed = cast(list[Any], d.pop("mixedFeed", UNSET))

        _mlb_debut_date = d.pop("mlbDebutDate", UNSET)
        mlb_debut_date: datetime.date | Unset
        if isinstance(_mlb_debut_date, Unset):
            mlb_debut_date = UNSET
        else:
            mlb_debut_date = isoparse(_mlb_debut_date).date()

        name_slug = d.pop("nameSlug", UNSET)

        name_title = d.pop("nameTitle", UNSET)

        note = d.pop("note", UNSET)

        _pitch_hand = d.pop("pitchHand", UNSET)
        pitch_hand: DynamicEnumRestObject | Unset
        if isinstance(_pitch_hand, Unset):
            pitch_hand = UNSET
        else:
            pitch_hand = DynamicEnumRestObject.from_dict(_pitch_hand)

        strike_zone_bottom = d.pop("strikeZoneBottom", UNSET)

        strike_zone_top = d.pop("strikeZoneTop", UNSET)

        _transactions = d.pop("transactions", UNSET)
        transactions: list[TransactionRestObject] | Unset = UNSET
        if _transactions is not UNSET:
            transactions = []
            for transactions_item_data in _transactions:
                transactions_item = TransactionRestObject.from_dict(
                    transactions_item_data
                )

                transactions.append(transactions_item)

        videos = cast(list[Any], d.pop("videos", UNSET))

        baseball_person_rest_object = cls(
            articles=articles,
            bat_side=bat_side,
            drafts=drafts,
            first_last_name=first_last_name,
            full_fml_name=full_fml_name,
            full_lfm_name=full_lfm_name,
            init_last_name=init_last_name,
            last_first_name=last_first_name,
            last_init_name=last_init_name,
            mixed_feed=mixed_feed,
            mlb_debut_date=mlb_debut_date,
            name_slug=name_slug,
            name_title=name_title,
            note=note,
            pitch_hand=pitch_hand,
            strike_zone_bottom=strike_zone_bottom,
            strike_zone_top=strike_zone_top,
            transactions=transactions,
            videos=videos,
        )

        baseball_person_rest_object.additional_properties = d
        return baseball_person_rest_object

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
