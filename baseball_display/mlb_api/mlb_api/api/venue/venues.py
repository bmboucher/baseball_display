from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    venue_ids: Any,
    sport_ids: Any,
    season: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["venueIds"] = venue_ids

    params["sportIds"] = sport_ids

    params["season"] = season

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    json_hydrate: list[str] | Unset = UNSET
    if not isinstance(hydrate, Unset):
        json_hydrate = hydrate

    params["hydrate"] = json_hydrate

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/venues",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 200:
        return None

    if response.status_code == 401:
        return None

    if response.status_code == 403:
        return None

    if response.status_code == 404:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    venue_ids: Any,
    sport_ids: Any,
    season: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View information for a venue based on venueId.

     **Description:**
     This endpoint returns venue directorial information for all available venues in the Stats API.

     **Return Includes:** Name and id

     **Required Parameters:** venueIds is required to run this call. However, sportIds and leagueIds
    must be called seperately

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/venues?venueIds=15

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/venues?venueIds=15&hydrate=location


    Args:
        venue_ids (Any):
        sport_ids (Any):
        season (str | Unset):
        fields (list[str] | Unset):
        hydrate (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        venue_ids=venue_ids,
        sport_ids=sport_ids,
        season=season,
        fields=fields,
        hydrate=hydrate,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    venue_ids: Any,
    sport_ids: Any,
    season: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View information for a venue based on venueId.

     **Description:**
     This endpoint returns venue directorial information for all available venues in the Stats API.

     **Return Includes:** Name and id

     **Required Parameters:** venueIds is required to run this call. However, sportIds and leagueIds
    must be called seperately

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/venues?venueIds=15

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/venues?venueIds=15&hydrate=location


    Args:
        venue_ids (Any):
        sport_ids (Any):
        season (str | Unset):
        fields (list[str] | Unset):
        hydrate (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        venue_ids=venue_ids,
        sport_ids=sport_ids,
        season=season,
        fields=fields,
        hydrate=hydrate,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
