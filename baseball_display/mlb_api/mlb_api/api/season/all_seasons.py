from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.seasons_rest_object import SeasonsRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    with_game_type_dates: int,
    sport_id: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["divisionId"] = division_id

    params["leagueId"] = league_id

    params["withGameTypeDates"] = with_game_type_dates

    params["sportId"] = sport_id

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/seasons/all",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SeasonsRestObject | None:
    if response.status_code == 200:
        response_200 = SeasonsRestObject.from_dict(response.json())

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
) -> Response[Any | SeasonsRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    with_game_type_dates: int,
    sport_id: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | SeasonsRestObject]:
    """View information for all seasons based on id.

     **Description:**
     This endpoint returns season information for all seasons based on id.

     **Return Includes:** Regular Season, Postseason start dates and end dates

     **Required Parameters:** sportId is required to run this call.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/seasons/all?sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        with_game_type_dates (int):
        sport_id (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SeasonsRestObject]
    """

    kwargs = _get_kwargs(
        division_id=division_id,
        league_id=league_id,
        with_game_type_dates=with_game_type_dates,
        sport_id=sport_id,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    with_game_type_dates: int,
    sport_id: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | SeasonsRestObject | None:
    """View information for all seasons based on id.

     **Description:**
     This endpoint returns season information for all seasons based on id.

     **Return Includes:** Regular Season, Postseason start dates and end dates

     **Required Parameters:** sportId is required to run this call.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/seasons/all?sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        with_game_type_dates (int):
        sport_id (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | SeasonsRestObject
    """

    return sync_detailed(
        client=client,
        division_id=division_id,
        league_id=league_id,
        with_game_type_dates=with_game_type_dates,
        sport_id=sport_id,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    with_game_type_dates: int,
    sport_id: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | SeasonsRestObject]:
    """View information for all seasons based on id.

     **Description:**
     This endpoint returns season information for all seasons based on id.

     **Return Includes:** Regular Season, Postseason start dates and end dates

     **Required Parameters:** sportId is required to run this call.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/seasons/all?sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        with_game_type_dates (int):
        sport_id (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SeasonsRestObject]
    """

    kwargs = _get_kwargs(
        division_id=division_id,
        league_id=league_id,
        with_game_type_dates=with_game_type_dates,
        sport_id=sport_id,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    with_game_type_dates: int,
    sport_id: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | SeasonsRestObject | None:
    """View information for all seasons based on id.

     **Description:**
     This endpoint returns season information for all seasons based on id.

     **Return Includes:** Regular Season, Postseason start dates and end dates

     **Required Parameters:** sportId is required to run this call.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/seasons/all?sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        with_game_type_dates (int):
        sport_id (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | SeasonsRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            division_id=division_id,
            league_id=league_id,
            with_game_type_dates=with_game_type_dates,
            sport_id=sport_id,
            fields=fields,
        )
    ).parsed
