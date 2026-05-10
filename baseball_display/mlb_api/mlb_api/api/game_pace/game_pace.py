from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.game_pace_league_list_id import GamePaceLeagueListId
from ...models.game_pace_org_type import GamePaceOrgType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    season: list[int],
    team_ids: list[int] | Unset = UNSET,
    league_ids: list[int] | Unset = UNSET,
    league_list_id: GamePaceLeagueListId | Unset = UNSET,
    sport_id: int | Unset = UNSET,
    game_type: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_ids: Any | Unset = UNSET,
    org_type: GamePaceOrgType | Unset = UNSET,
    include_children: bool | Unset = False,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_season = season

    params["season"] = json_season

    json_team_ids: list[int] | Unset = UNSET
    if not isinstance(team_ids, Unset):
        json_team_ids = team_ids

    params["teamIds"] = json_team_ids

    json_league_ids: list[int] | Unset = UNSET
    if not isinstance(league_ids, Unset):
        json_league_ids = league_ids

    params["leagueIds"] = json_league_ids

    json_league_list_id: str | Unset = UNSET
    if not isinstance(league_list_id, Unset):
        json_league_list_id = league_list_id.value

    params["leagueListId"] = json_league_list_id

    params["sportId"] = sport_id

    json_game_type: list[str] | Unset = UNSET
    if not isinstance(game_type, Unset):
        json_game_type = game_type

    params["gameType"] = json_game_type

    params["startDate"] = start_date

    params["endDate"] = end_date

    params["venueIds"] = venue_ids

    json_org_type: str | Unset = UNSET
    if not isinstance(org_type, Unset):
        json_org_type = org_type.value

    params["orgType"] = json_org_type

    params["includeChildren"] = include_children

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/gamePace",
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
    season: list[int],
    team_ids: list[int] | Unset = UNSET,
    league_ids: list[int] | Unset = UNSET,
    league_list_id: GamePaceLeagueListId | Unset = UNSET,
    sport_id: int | Unset = UNSET,
    game_type: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_ids: Any | Unset = UNSET,
    org_type: GamePaceOrgType | Unset = UNSET,
    include_children: bool | Unset = False,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View time of game info.


    **Description:**
    This endpoint returns pace of game metrics for specific sport, league or team.

    **Return Includes:** Time of game, time per hit, totalHits etc....

    **Required Parameters:** season is required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/gamePace?season=2018


    deprecated: false

    Args:
        season (list[int]):
        team_ids (list[int] | Unset):
        league_ids (list[int] | Unset):
        league_list_id (GamePaceLeagueListId | Unset):
        sport_id (int | Unset):
        game_type (list[str] | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        venue_ids (Any | Unset):
        org_type (GamePaceOrgType | Unset):
        include_children (bool | Unset):  Default: False.
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        team_ids=team_ids,
        league_ids=league_ids,
        league_list_id=league_list_id,
        sport_id=sport_id,
        game_type=game_type,
        start_date=start_date,
        end_date=end_date,
        venue_ids=venue_ids,
        org_type=org_type,
        include_children=include_children,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    season: list[int],
    team_ids: list[int] | Unset = UNSET,
    league_ids: list[int] | Unset = UNSET,
    league_list_id: GamePaceLeagueListId | Unset = UNSET,
    sport_id: int | Unset = UNSET,
    game_type: list[str] | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_ids: Any | Unset = UNSET,
    org_type: GamePaceOrgType | Unset = UNSET,
    include_children: bool | Unset = False,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View time of game info.


    **Description:**
    This endpoint returns pace of game metrics for specific sport, league or team.

    **Return Includes:** Time of game, time per hit, totalHits etc....

    **Required Parameters:** season is required to run this call.

    ---
    **Example of call with required parameters**

    1. https://statsapi.mlb.com/api/v1/gamePace?season=2018


    deprecated: false

    Args:
        season (list[int]):
        team_ids (list[int] | Unset):
        league_ids (list[int] | Unset):
        league_list_id (GamePaceLeagueListId | Unset):
        sport_id (int | Unset):
        game_type (list[str] | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        venue_ids (Any | Unset):
        org_type (GamePaceOrgType | Unset):
        include_children (bool | Unset):  Default: False.
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        team_ids=team_ids,
        league_ids=league_ids,
        league_list_id=league_list_id,
        sport_id=sport_id,
        game_type=game_type,
        start_date=start_date,
        end_date=end_date,
        venue_ids=venue_ids,
        org_type=org_type,
        include_children=include_children,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
