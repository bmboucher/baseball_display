from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.people_rest_object import PeopleRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sport_id: str,
    *,
    season: str,
    game_type: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["season"] = season

    params["gameType"] = game_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sports/{sport_id}/players".format(
            sport_id=quote(str(sport_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PeopleRestObject | None:
    if response.status_code == 200:
        response_200 = PeopleRestObject.from_dict(response.json())

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
) -> Response[Any | PeopleRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sport_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    game_type: str | Unset = UNSET,
) -> Response[Any | PeopleRestObject]:
    """View information on a players for a given sportId.

     **Description:**
     This endpoint returns player information for all players in a given sport.

     **Return Includes:** Biographical information and strikezone size.

     **Required Parameters:** sportId and season are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/sports/1/players?season=2018


     ---

     **Example of call with all parameters**

       https://statsapi.mlb.com/api/v1/sports/1/players?season=2017&gameType=W

    Args:
        sport_id (str):
        season (str):
        game_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PeopleRestObject]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        season=season,
        game_type=game_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sport_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    game_type: str | Unset = UNSET,
) -> Any | PeopleRestObject | None:
    """View information on a players for a given sportId.

     **Description:**
     This endpoint returns player information for all players in a given sport.

     **Return Includes:** Biographical information and strikezone size.

     **Required Parameters:** sportId and season are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/sports/1/players?season=2018


     ---

     **Example of call with all parameters**

       https://statsapi.mlb.com/api/v1/sports/1/players?season=2017&gameType=W

    Args:
        sport_id (str):
        season (str):
        game_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PeopleRestObject
    """

    return sync_detailed(
        sport_id=sport_id,
        client=client,
        season=season,
        game_type=game_type,
    ).parsed


async def asyncio_detailed(
    sport_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    game_type: str | Unset = UNSET,
) -> Response[Any | PeopleRestObject]:
    """View information on a players for a given sportId.

     **Description:**
     This endpoint returns player information for all players in a given sport.

     **Return Includes:** Biographical information and strikezone size.

     **Required Parameters:** sportId and season are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/sports/1/players?season=2018


     ---

     **Example of call with all parameters**

       https://statsapi.mlb.com/api/v1/sports/1/players?season=2017&gameType=W

    Args:
        sport_id (str):
        season (str):
        game_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PeopleRestObject]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        season=season,
        game_type=game_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sport_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    game_type: str | Unset = UNSET,
) -> Any | PeopleRestObject | None:
    """View information on a players for a given sportId.

     **Description:**
     This endpoint returns player information for all players in a given sport.

     **Return Includes:** Biographical information and strikezone size.

     **Required Parameters:** sportId and season are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/sports/1/players?season=2018


     ---

     **Example of call with all parameters**

       https://statsapi.mlb.com/api/v1/sports/1/players?season=2017&gameType=W

    Args:
        sport_id (str):
        season (str):
        game_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PeopleRestObject
    """

    return (
        await asyncio_detailed(
            sport_id=sport_id,
            client=client,
            season=season,
            game_type=game_type,
        )
    ).parsed
