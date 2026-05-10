from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.game_data_game_rest_object import GameDataGameRestObject
    from ..models.game_date_time_rest_object import GameDateTimeRestObject
    from ..models.game_status_rest_object import GameStatusRestObject
    from ..models.venue_rest_object import VenueRestObject


T = TypeVar("T", bound="GameDataRestObject")


@_attrs_define
class GameDataRestObject:
    """
    Attributes:
        datetime_ (GameDateTimeRestObject | Unset):
        game (GameDataGameRestObject | Unset):
        status (GameStatusRestObject | Unset):
        venue (VenueRestObject | Unset):
    """

    datetime_: GameDateTimeRestObject | Unset = UNSET
    game: GameDataGameRestObject | Unset = UNSET
    status: GameStatusRestObject | Unset = UNSET
    venue: VenueRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.game_data_game_rest_object import GameDataGameRestObject
        from ..models.game_date_time_rest_object import GameDateTimeRestObject
        from ..models.game_status_rest_object import GameStatusRestObject
        from ..models.venue_rest_object import VenueRestObject

        datetime_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.datetime_, Unset):
            datetime_ = self.datetime_.to_dict()

        game: dict[str, Any] | Unset = UNSET
        if not isinstance(self.game, Unset):
            game = self.game.to_dict()

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        venue: dict[str, Any] | Unset = UNSET
        if not isinstance(self.venue, Unset):
            venue = self.venue.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_
        if game is not UNSET:
            field_dict["game"] = game
        if status is not UNSET:
            field_dict["status"] = status
        if venue is not UNSET:
            field_dict["venue"] = venue

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.game_data_game_rest_object import GameDataGameRestObject
        from ..models.game_date_time_rest_object import GameDateTimeRestObject
        from ..models.game_status_rest_object import GameStatusRestObject
        from ..models.venue_rest_object import VenueRestObject

        d = dict(src_dict)
        _datetime_ = d.pop("datetime", UNSET)
        datetime_: GameDateTimeRestObject | Unset
        if isinstance(_datetime_, Unset):
            datetime_ = UNSET
        else:
            datetime_ = GameDateTimeRestObject.from_dict(_datetime_)

        _game = d.pop("game", UNSET)
        game: GameDataGameRestObject | Unset
        if isinstance(_game, Unset):
            game = UNSET
        else:
            game = GameDataGameRestObject.from_dict(_game)

        _status = d.pop("status", UNSET)
        status: GameStatusRestObject | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GameStatusRestObject.from_dict(_status)

        _venue = d.pop("venue", UNSET)
        venue: VenueRestObject | Unset
        if isinstance(_venue, Unset):
            venue = UNSET
        else:
            venue = VenueRestObject.from_dict(_venue)

        game_data_rest_object = cls(
            datetime_=datetime_,
            game=game,
            status=status,
            venue=venue,
        )

        game_data_rest_object.additional_properties = d
        return game_data_rest_object

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
