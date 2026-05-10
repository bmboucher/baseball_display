from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_winner_rest_object import AwardWinnerRestObject


T = TypeVar("T", bound="AwardResultRestObject")


@_attrs_define
class AwardResultRestObject:
    """
    Attributes:
        season_id (int | Unset):
        winners (list[AwardWinnerRestObject] | Unset):
    """

    season_id: int | Unset = UNSET
    winners: list[AwardWinnerRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_winner_rest_object import AwardWinnerRestObject

        season_id = self.season_id

        winners: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.winners, Unset):
            winners = []
            for winners_item_data in self.winners:
                winners_item = winners_item_data.to_dict()
                winners.append(winners_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if season_id is not UNSET:
            field_dict["seasonId"] = season_id
        if winners is not UNSET:
            field_dict["winners"] = winners

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_winner_rest_object import AwardWinnerRestObject

        d = dict(src_dict)
        season_id = d.pop("seasonId", UNSET)

        _winners = d.pop("winners", UNSET)
        winners: list[AwardWinnerRestObject] | Unset = UNSET
        if _winners is not UNSET:
            winners = []
            for winners_item_data in _winners:
                winners_item = AwardWinnerRestObject.from_dict(winners_item_data)

                winners.append(winners_item)

        award_result_rest_object = cls(
            season_id=season_id,
            winners=winners,
        )

        award_result_rest_object.additional_properties = d
        return award_result_rest_object

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
