from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_ids: str,
    sport_id: int | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["teamIds"] = team_ids

    params["sportId"] = sport_id

    params["season"] = season

    json_hydrate: list[str] | Unset = UNSET
    if not isinstance(hydrate, Unset):
        json_hydrate = hydrate

    params["hydrate"] = json_hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/affiliates",
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
    team_ids: str,
    sport_id: int | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View a directory of affiliates for a given team.

     **Description:**
     This endpoint returns a directory of affiliates for a given team based on teamIds,leagueId,sportId
    and gameType.

     **Return Includes:** League,division,sport and venue information for each team.

     **Required Parameters:** teamIds is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=147

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=147&hydrate=league

    Args:
        team_ids (str):
        sport_id (int | Unset):
        season (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        team_ids=team_ids,
        sport_id=sport_id,
        season=season,
        hydrate=hydrate,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    team_ids: str,
    sport_id: int | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View a directory of affiliates for a given team.

     **Description:**
     This endpoint returns a directory of affiliates for a given team based on teamIds,leagueId,sportId
    and gameType.

     **Return Includes:** League,division,sport and venue information for each team.

     **Required Parameters:** teamIds is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=147

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=147&hydrate=league

    Args:
        team_ids (str):
        sport_id (int | Unset):
        season (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        team_ids=team_ids,
        sport_id=sport_id,
        season=season,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
