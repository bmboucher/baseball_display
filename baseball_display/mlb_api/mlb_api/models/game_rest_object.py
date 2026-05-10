from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.game_data_rest_object import GameDataRestObject
    from ..models.game_live_data_rest_object import GameLiveDataRestObject
    from ..models.game_meta_data_rest_object import GameMetaDataRestObject


T = TypeVar("T", bound="GameRestObject")


@_attrs_define
class GameRestObject:
    """
    Attributes:
        game_data (GameDataRestObject | Unset):
        game_pk (int | Unset): Unique Primary Key Representing a Game
        link (str | Unset): Link to full resource
        live_data (GameLiveDataRestObject | Unset):
        meta_data (GameMetaDataRestObject | Unset):
    """

    game_data: GameDataRestObject | Unset = UNSET
    game_pk: int | Unset = UNSET
    link: str | Unset = UNSET
    live_data: GameLiveDataRestObject | Unset = UNSET
    meta_data: GameMetaDataRestObject | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.game_data_rest_object import GameDataRestObject
        from ..models.game_live_data_rest_object import GameLiveDataRestObject
        from ..models.game_meta_data_rest_object import GameMetaDataRestObject

        game_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.game_data, Unset):
            game_data = self.game_data.to_dict()

        game_pk = self.game_pk

        link = self.link

        live_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.live_data, Unset):
            live_data = self.live_data.to_dict()

        meta_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta_data, Unset):
            meta_data = self.meta_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if game_data is not UNSET:
            field_dict["gameData"] = game_data
        if game_pk is not UNSET:
            field_dict["gamePk"] = game_pk
        if link is not UNSET:
            field_dict["link"] = link
        if live_data is not UNSET:
            field_dict["liveData"] = live_data
        if meta_data is not UNSET:
            field_dict["metaData"] = meta_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.game_data_rest_object import GameDataRestObject
        from ..models.game_live_data_rest_object import GameLiveDataRestObject
        from ..models.game_meta_data_rest_object import GameMetaDataRestObject

        d = dict(src_dict)
        _game_data = d.pop("gameData", UNSET)
        game_data: GameDataRestObject | Unset
        if isinstance(_game_data, Unset):
            game_data = UNSET
        else:
            game_data = GameDataRestObject.from_dict(_game_data)

        game_pk = d.pop("gamePk", UNSET)

        link = d.pop("link", UNSET)

        _live_data = d.pop("liveData", UNSET)
        live_data: GameLiveDataRestObject | Unset
        if isinstance(_live_data, Unset):
            live_data = UNSET
        else:
            live_data = GameLiveDataRestObject.from_dict(_live_data)

        _meta_data = d.pop("metaData", UNSET)
        meta_data: GameMetaDataRestObject | Unset
        if isinstance(_meta_data, Unset):
            meta_data = UNSET
        else:
            meta_data = GameMetaDataRestObject.from_dict(_meta_data)

        game_rest_object = cls(
            game_data=game_data,
            game_pk=game_pk,
            link=link,
            live_data=live_data,
            meta_data=meta_data,
        )

        game_rest_object.additional_properties = d
        return game_rest_object

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
