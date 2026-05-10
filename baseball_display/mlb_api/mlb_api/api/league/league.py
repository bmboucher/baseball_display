from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sport_id: str,
    league_ids: str,
    seasons: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["sportId"] = sport_id

    params["leagueIds"] = league_ids

    params["seasons"] = seasons

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/league",
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
    sport_id: str,
    league_ids: str,
    seasons: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View league information.

     **Description:**
    This endpoint returns league information data based on sportId,leagueId,or year.

    **Return Includes:** Regular Season Start/End Date, Post  Season Start/End Date, leagueId.

    **Required Parameters:** SportId or LeagueId are required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/league?sportId=1
    2. https://statsapi.mlb.com/api/v1/league?leagueIds=103
    <br> </br>
    **Blank season value defaults to current year.**

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/league?leagueIds=103&seasons=2018

    Args:
        sport_id (str):
        league_ids (str):
        seasons (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        league_ids=league_ids,
        seasons=seasons,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    sport_id: str,
    league_ids: str,
    seasons: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View league information.

     **Description:**
    This endpoint returns league information data based on sportId,leagueId,or year.

    **Return Includes:** Regular Season Start/End Date, Post  Season Start/End Date, leagueId.

    **Required Parameters:** SportId or LeagueId are required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/league?sportId=1
    2. https://statsapi.mlb.com/api/v1/league?leagueIds=103
    <br> </br>
    **Blank season value defaults to current year.**

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/league?leagueIds=103&seasons=2018

    Args:
        sport_id (str):
        league_ids (str):
        seasons (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        league_ids=league_ids,
        seasons=seasons,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
