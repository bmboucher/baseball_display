from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    game_types: Any | Unset = UNSET,
    series_number: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["gameTypes"] = game_types

    params["seriesNumber"] = series_number

    params["teamId"] = team_id

    params["sportId"] = sport_id

    params["season"] = season

    params["hydrate"] = hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/schedule/postseason",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 200:
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
    game_types: Any | Unset = UNSET,
    series_number: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View postseason schedule info.

     **Description:**
     This endpoint returns postseason schedules for a given year.

     **Return Includes:** Team information, date of play and game status.

     **Required Parameters:** There are no required parameters to run this call. Blank call
    (https://statsapi.mlb.com/api/v1/schedule/postseason) will return current year's postseason schedule

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/schedule/postseason?hydrate=hydrations,linescore&season=2017

    Args:
        game_types (Any | Unset):
        series_number (int | Unset):
        team_id (int | Unset):
        sport_id (str | Unset):
        season (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_types=game_types,
        series_number=series_number,
        team_id=team_id,
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
    game_types: Any | Unset = UNSET,
    series_number: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    season: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View postseason schedule info.

     **Description:**
     This endpoint returns postseason schedules for a given year.

     **Return Includes:** Team information, date of play and game status.

     **Required Parameters:** There are no required parameters to run this call. Blank call
    (https://statsapi.mlb.com/api/v1/schedule/postseason) will return current year's postseason schedule

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/schedule/postseason?hydrate=hydrations,linescore&season=2017

    Args:
        game_types (Any | Unset):
        series_number (int | Unset):
        team_id (int | Unset):
        sport_id (str | Unset):
        season (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_types=game_types,
        series_number=series_number,
        team_id=team_id,
        sport_id=sport_id,
        season=season,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
