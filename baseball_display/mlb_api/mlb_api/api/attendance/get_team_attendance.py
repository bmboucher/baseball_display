from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_team_attendance_league_list_id import GetTeamAttendanceLeagueListId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    team_id: list[int],
    league_id: list[int],
    season: list[int] | Unset = UNSET,
    date: str | Unset = UNSET,
    league_list_id: GetTeamAttendanceLeagueListId,
    game_type: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_team_id = team_id

    params["teamId"] = json_team_id

    json_league_id = league_id

    params["leagueId"] = json_league_id

    json_season: list[int] | Unset = UNSET
    if not isinstance(season, Unset):
        json_season = season

    params["season"] = json_season

    params["date"] = date

    json_league_list_id = league_list_id.value
    params["leagueListId"] = json_league_list_id

    json_game_type: list[str] | Unset = UNSET
    if not isinstance(game_type, Unset):
        json_game_type = game_type

    params["gameType"] = json_game_type

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params["startDate"] = start_date

    params["endDate"] = end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/attendance",
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
    team_id: list[int],
    league_id: list[int],
    season: list[int] | Unset = UNSET,
    date: str | Unset = UNSET,
    league_list_id: GetTeamAttendanceLeagueListId,
    game_type: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
) -> Response[Any]:
    """View attendance information.

     **Description:**
    This endpoint returns attendance  data based on teamId, leagueId, or leagueListId.

    **Return Includes:** attendance total, splits for high/low & home/away, and gameType.

    **Required Parameters:** SportId or LeagueId are required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/attendance?teamId=110
    2. https://statsapi.mlb.com/api/v1/attendance?leagueId=103
    3. https://statsapi.mlb.com/api/v1/attendance?leagueListId=mlb
    <br> </br>

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/attendance?teamId=110&leagueId=103&season=2014&leagueListId=mlb&game
    Type=D

    Args:
        team_id (list[int]):
        league_id (list[int]):
        season (list[int] | Unset):
        date (str | Unset):
        league_list_id (GetTeamAttendanceLeagueListId):
        game_type (list[str] | Unset):
        fields (list[str] | Unset):
        start_date (str | Unset):
        end_date (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        league_id=league_id,
        season=season,
        date=date,
        league_list_id=league_list_id,
        game_type=game_type,
        fields=fields,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    team_id: list[int],
    league_id: list[int],
    season: list[int] | Unset = UNSET,
    date: str | Unset = UNSET,
    league_list_id: GetTeamAttendanceLeagueListId,
    game_type: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
) -> Response[Any]:
    """View attendance information.

     **Description:**
    This endpoint returns attendance  data based on teamId, leagueId, or leagueListId.

    **Return Includes:** attendance total, splits for high/low & home/away, and gameType.

    **Required Parameters:** SportId or LeagueId are required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/attendance?teamId=110
    2. https://statsapi.mlb.com/api/v1/attendance?leagueId=103
    3. https://statsapi.mlb.com/api/v1/attendance?leagueListId=mlb
    <br> </br>

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/attendance?teamId=110&leagueId=103&season=2014&leagueListId=mlb&game
    Type=D

    Args:
        team_id (list[int]):
        league_id (list[int]):
        season (list[int] | Unset):
        date (str | Unset):
        league_list_id (GetTeamAttendanceLeagueListId):
        game_type (list[str] | Unset):
        fields (list[str] | Unset):
        start_date (str | Unset):
        end_date (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        league_id=league_id,
        season=season,
        date=date,
        league_list_id=league_list_id,
        game_type=game_type,
        fields=fields,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
