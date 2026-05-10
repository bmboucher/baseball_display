from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.free_agent_rest_object import FreeAgentRestObject


T = TypeVar("T", bound="FreeAgentListRestObject")


@_attrs_define
class FreeAgentListRestObject:
    """
    Attributes:
        free_agents (list[FreeAgentRestObject] | Unset):
        season (str | Unset):
    """

    free_agents: list[FreeAgentRestObject] | Unset = UNSET
    season: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.free_agent_rest_object import FreeAgentRestObject

        free_agents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.free_agents, Unset):
            free_agents = []
            for free_agents_item_data in self.free_agents:
                free_agents_item = free_agents_item_data.to_dict()
                free_agents.append(free_agents_item)

        season = self.season

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if free_agents is not UNSET:
            field_dict["freeAgents"] = free_agents
        if season is not UNSET:
            field_dict["season"] = season

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.free_agent_rest_object import FreeAgentRestObject

        d = dict(src_dict)
        _free_agents = d.pop("freeAgents", UNSET)
        free_agents: list[FreeAgentRestObject] | Unset = UNSET
        if _free_agents is not UNSET:
            free_agents = []
            for free_agents_item_data in _free_agents:
                free_agents_item = FreeAgentRestObject.from_dict(free_agents_item_data)

                free_agents.append(free_agents_item)

        season = d.pop("season", UNSET)

        free_agent_list_rest_object = cls(
            free_agents=free_agents,
            season=season,
        )

        free_agent_list_rest_object.additional_properties = d
        return free_agent_list_rest_object

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
