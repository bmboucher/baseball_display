from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    schedule_type: Any | Unset = UNSET,
    event_types: Any | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    team_id: Any | Unset = UNSET,
    league_id: Any | Unset = UNSET,
    sport_id: Any,
    game_pks: Any,
    venue_ids: Any | Unset = UNSET,
    game_types: Any | Unset = UNSET,
    date: str | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    opponent_id: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["scheduleType"] = schedule_type

    params["eventTypes"] = event_types

    params["hydrate"] = hydrate

    params["teamId"] = team_id

    params["leagueId"] = league_id

    params["sportId"] = sport_id

    params["gamePks"] = game_pks

    params["venueIds"] = venue_ids

    params["gameTypes"] = game_types

    params["date"] = date

    params["startDate"] = start_date

    params["endDate"] = end_date

    params["opponentId"] = opponent_id

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/schedule/",
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
    schedule_type: Any | Unset = UNSET,
    event_types: Any | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    team_id: Any | Unset = UNSET,
    league_id: Any | Unset = UNSET,
    sport_id: Any,
    game_pks: Any,
    venue_ids: Any | Unset = UNSET,
    game_types: Any | Unset = UNSET,
    date: str | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    opponent_id: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View schedule info based on scheduleType.

     **Description:**
     This endpoint returns all schedules based on a particular scheduleType.

     **Return Includes:** Game and event data.

     **Required Parameters:** sportId or gamePk(s) are required to run this call

     **Hydrations:** This endpoint can accept the hydrations query parameter.

     ---
     **Example of call with required parameters**
      1. https://statsapi.mlb.com/api/v1/schedule?sportId=1
      2. https://statsapi.mlb.com/api/v1/schedule/?sportId=1&gamePk=534262

     **If no gamePk or startDate/endDate are given then call will populate for current date**

     ---
     **Example of call with hydration parameters**
     https://statsapi.mlb.com/api/v1/schedule/?sportId=1&gamePk=534262&hydrate=linescore

    Args:
        schedule_type (Any | Unset):
        event_types (Any | Unset):
        hydrate (Any | Unset):
        team_id (Any | Unset):
        league_id (Any | Unset):
        sport_id (Any):
        game_pks (Any):
        venue_ids (Any | Unset):
        game_types (Any | Unset):
        date (str | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        opponent_id (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        schedule_type=schedule_type,
        event_types=event_types,
        hydrate=hydrate,
        team_id=team_id,
        league_id=league_id,
        sport_id=sport_id,
        game_pks=game_pks,
        venue_ids=venue_ids,
        game_types=game_types,
        date=date,
        start_date=start_date,
        end_date=end_date,
        opponent_id=opponent_id,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    schedule_type: Any | Unset = UNSET,
    event_types: Any | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    team_id: Any | Unset = UNSET,
    league_id: Any | Unset = UNSET,
    sport_id: Any,
    game_pks: Any,
    venue_ids: Any | Unset = UNSET,
    game_types: Any | Unset = UNSET,
    date: str | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    opponent_id: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View schedule info based on scheduleType.

     **Description:**
     This endpoint returns all schedules based on a particular scheduleType.

     **Return Includes:** Game and event data.

     **Required Parameters:** sportId or gamePk(s) are required to run this call

     **Hydrations:** This endpoint can accept the hydrations query parameter.

     ---
     **Example of call with required parameters**
      1. https://statsapi.mlb.com/api/v1/schedule?sportId=1
      2. https://statsapi.mlb.com/api/v1/schedule/?sportId=1&gamePk=534262

     **If no gamePk or startDate/endDate are given then call will populate for current date**

     ---
     **Example of call with hydration parameters**
     https://statsapi.mlb.com/api/v1/schedule/?sportId=1&gamePk=534262&hydrate=linescore

    Args:
        schedule_type (Any | Unset):
        event_types (Any | Unset):
        hydrate (Any | Unset):
        team_id (Any | Unset):
        league_id (Any | Unset):
        sport_id (Any):
        game_pks (Any):
        venue_ids (Any | Unset):
        game_types (Any | Unset):
        date (str | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        opponent_id (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        schedule_type=schedule_type,
        event_types=event_types,
        hydrate=hydrate,
        team_id=team_id,
        league_id=league_id,
        sport_id=sport_id,
        game_pks=game_pks,
        venue_ids=venue_ids,
        game_types=game_types,
        date=date,
        start_date=start_date,
        end_date=end_date,
        opponent_id=opponent_id,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
