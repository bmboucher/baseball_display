from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_streaks_streak_span import GetStreaksStreakSpan
from ...models.get_streaks_streak_type import GetStreaksStreakType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    streak_type: GetStreaksStreakType,
    streak_span: GetStreaksStreakSpan,
    game_type: str | Unset = UNSET,
    season: str,
    sport_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_streak_type = streak_type.value
    params["streakType"] = json_streak_type

    json_streak_span = streak_span.value
    params["streakSpan"] = json_streak_span

    params["gameType"] = game_type

    params["season"] = season

    params["sportId"] = sport_id

    params["limit"] = limit

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
        "url": "/v1/stats/streaks",
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
    streak_type: GetStreaksStreakType,
    streak_span: GetStreaksStreakSpan,
    game_type: str | Unset = UNSET,
    season: str,
    sport_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View statistical streaks for a given season

     **Description:**
     This endpoint returns statistical streaks based on streakType,streakSpan,gameType,season, &
    sportId.

     **Return Includes:** biographical and statistical information for a group of players.

     **Required Parameters:** streakType,streakSpan,gameType,season, sportId & limit

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with hydration parameters**

     http://statsapi.mlb.com/api/v1/stats/streaks?gameType=R&streakSpan=season&streakType=hittingStreakO
    verall&season=2018&sportId=1&limit=10&hydrate=person(stats(type=season,season=2018))

    Args:
        streak_type (GetStreaksStreakType):
        streak_span (GetStreaksStreakSpan):
        game_type (str | Unset):
        season (str):
        sport_id (str | Unset):
        limit (int | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        streak_type=streak_type,
        streak_span=streak_span,
        game_type=game_type,
        season=season,
        sport_id=sport_id,
        limit=limit,
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
    streak_type: GetStreaksStreakType,
    streak_span: GetStreaksStreakSpan,
    game_type: str | Unset = UNSET,
    season: str,
    sport_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View statistical streaks for a given season

     **Description:**
     This endpoint returns statistical streaks based on streakType,streakSpan,gameType,season, &
    sportId.

     **Return Includes:** biographical and statistical information for a group of players.

     **Required Parameters:** streakType,streakSpan,gameType,season, sportId & limit

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with hydration parameters**

     http://statsapi.mlb.com/api/v1/stats/streaks?gameType=R&streakSpan=season&streakType=hittingStreakO
    verall&season=2018&sportId=1&limit=10&hydrate=person(stats(type=season,season=2018))

    Args:
        streak_type (GetStreaksStreakType):
        streak_span (GetStreaksStreakSpan):
        game_type (str | Unset):
        season (str):
        sport_id (str | Unset):
        limit (int | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        streak_type=streak_type,
        streak_span=streak_span,
        game_type=game_type,
        season=season,
        sport_id=sport_id,
        limit=limit,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
