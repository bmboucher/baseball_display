from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.standings_rest_object import StandingsRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    league_id: str,
    season: str,
    standings_types: str | Unset = UNSET,
    date: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["leagueId"] = league_id

    params["season"] = season

    params["standingsTypes"] = standings_types

    params["date"] = date

    params["hydrate"] = hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/standings",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | StandingsRestObject | None:
    if response.status_code == 200:
        response_200 = StandingsRestObject.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | StandingsRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    league_id: str,
    season: str,
    standings_types: str | Unset = UNSET,
    date: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | StandingsRestObject]:
    """View standings for a league.

     **Description:**
     This endpoint returns standings information for a given league.

     **Return Includes:** Team and standing information.

     **Required Parameters:** leagueId and season are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018

       **Call defaults to regularSeason standings**

     ---

     **Example of call with hydrated parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018&standingsTypes=wildCard,regula
    rSeason&hydrate=team(league)

    Args:
        league_id (str):
        season (str):
        standings_types (str | Unset):
        date (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | StandingsRestObject]
    """

    kwargs = _get_kwargs(
        league_id=league_id,
        season=season,
        standings_types=standings_types,
        date=date,
        hydrate=hydrate,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    league_id: str,
    season: str,
    standings_types: str | Unset = UNSET,
    date: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | StandingsRestObject | None:
    """View standings for a league.

     **Description:**
     This endpoint returns standings information for a given league.

     **Return Includes:** Team and standing information.

     **Required Parameters:** leagueId and season are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018

       **Call defaults to regularSeason standings**

     ---

     **Example of call with hydrated parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018&standingsTypes=wildCard,regula
    rSeason&hydrate=team(league)

    Args:
        league_id (str):
        season (str):
        standings_types (str | Unset):
        date (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | StandingsRestObject
    """

    return sync_detailed(
        client=client,
        league_id=league_id,
        season=season,
        standings_types=standings_types,
        date=date,
        hydrate=hydrate,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    league_id: str,
    season: str,
    standings_types: str | Unset = UNSET,
    date: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | StandingsRestObject]:
    """View standings for a league.

     **Description:**
     This endpoint returns standings information for a given league.

     **Return Includes:** Team and standing information.

     **Required Parameters:** leagueId and season are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018

       **Call defaults to regularSeason standings**

     ---

     **Example of call with hydrated parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018&standingsTypes=wildCard,regula
    rSeason&hydrate=team(league)

    Args:
        league_id (str):
        season (str):
        standings_types (str | Unset):
        date (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | StandingsRestObject]
    """

    kwargs = _get_kwargs(
        league_id=league_id,
        season=season,
        standings_types=standings_types,
        date=date,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    league_id: str,
    season: str,
    standings_types: str | Unset = UNSET,
    date: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | StandingsRestObject | None:
    """View standings for a league.

     **Description:**
     This endpoint returns standings information for a given league.

     **Return Includes:** Team and standing information.

     **Required Parameters:** leagueId and season are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018

       **Call defaults to regularSeason standings**

     ---

     **Example of call with hydrated parameters**

       https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018&standingsTypes=wildCard,regula
    rSeason&hydrate=team(league)

    Args:
        league_id (str):
        season (str):
        standings_types (str | Unset):
        date (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | StandingsRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            league_id=league_id,
            season=season,
            standings_types=standings_types,
            date=date,
            hydrate=hydrate,
            fields=fields,
        )
    ).parsed
