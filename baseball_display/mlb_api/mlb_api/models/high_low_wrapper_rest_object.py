from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, TextIO, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.high_low_container_rest_object import HighLowContainerRestObject


T = TypeVar("T", bound="HighLowWrapperRestObject")


@_attrs_define
class HighLowWrapperRestObject:
    """
    Attributes:
        high_low_results (list[HighLowContainerRestObject] | Unset):
    """

    high_low_results: list[HighLowContainerRestObject] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.high_low_container_rest_object import HighLowContainerRestObject

        high_low_results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.high_low_results, Unset):
            high_low_results = []
            for high_low_results_item_data in self.high_low_results:
                high_low_results_item = high_low_results_item_data.to_dict()
                high_low_results.append(high_low_results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if high_low_results is not UNSET:
            field_dict["highLowResults"] = high_low_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.high_low_container_rest_object import HighLowContainerRestObject

        d = dict(src_dict)
        _high_low_results = d.pop("highLowResults", UNSET)
        high_low_results: list[HighLowContainerRestObject] | Unset = UNSET
        if _high_low_results is not UNSET:
            high_low_results = []
            for high_low_results_item_data in _high_low_results:
                high_low_results_item = HighLowContainerRestObject.from_dict(
                    high_low_results_item_data
                )

                high_low_results.append(high_low_results_item)

        high_low_wrapper_rest_object = cls(
            high_low_results=high_low_results,
        )

        high_low_wrapper_rest_object.additional_properties = d
        return high_low_wrapper_rest_object

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
