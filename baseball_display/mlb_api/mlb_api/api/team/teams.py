from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    season: str | Unset = UNSET,
    active_status: str | Unset = UNSET,
    all_star_statuses: str | Unset = UNSET,
    league_ids: str | Unset = UNSET,
    sport_ids: str | Unset = UNSET,
    game_type: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["season"] = season

    params["activeStatus"] = active_status

    params["allStarStatuses"] = all_star_statuses

    params["leagueIds"] = league_ids

    params["sportIds"] = sport_ids

    params["gameType"] = game_type

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
        "url": "/v1/teams",
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
    season: str | Unset = UNSET,
    active_status: str | Unset = UNSET,
    all_star_statuses: str | Unset = UNSET,
    league_ids: str | Unset = UNSET,
    sport_ids: str | Unset = UNSET,
    game_type: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View directory of team(s).

     **Description:**
     This endpoint returns team information based on year,leagueId,sportId and gameType.

     **Return Includes:** League,division,sport and venue information for each team.

     **Required Parameters:** No parameters are required to run this call. However, sportIds and
    leagueIds must be called seperately

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams?season=2018&sportId=1&hydrate=league

    Args:
        season (str | Unset):
        active_status (str | Unset):
        all_star_statuses (str | Unset):
        league_ids (str | Unset):
        sport_ids (str | Unset):
        game_type (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        active_status=active_status,
        all_star_statuses=all_star_statuses,
        league_ids=league_ids,
        sport_ids=sport_ids,
        game_type=game_type,
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
    season: str | Unset = UNSET,
    active_status: str | Unset = UNSET,
    all_star_statuses: str | Unset = UNSET,
    league_ids: str | Unset = UNSET,
    sport_ids: str | Unset = UNSET,
    game_type: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View directory of team(s).

     **Description:**
     This endpoint returns team information based on year,leagueId,sportId and gameType.

     **Return Includes:** League,division,sport and venue information for each team.

     **Required Parameters:** No parameters are required to run this call. However, sportIds and
    leagueIds must be called seperately

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams?season=2018&sportId=1&hydrate=league

    Args:
        season (str | Unset):
        active_status (str | Unset):
        all_star_statuses (str | Unset):
        league_ids (str | Unset):
        sport_ids (str | Unset):
        game_type (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        active_status=active_status,
        all_star_statuses=all_star_statuses,
        league_ids=league_ids,
        sport_ids=sport_ids,
        game_type=game_type,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
