from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.stats_position import StatsPosition
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    stats: Any,
    player_pool: str | Unset = UNSET,
    position: StatsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    order: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["stats"] = stats

    params["playerPool"] = player_pool

    json_position: str | Unset = UNSET
    if not isinstance(position, Unset):
        json_position = position.value

    params["position"] = json_position

    params["teamId"] = team_id

    params["leagueId"] = league_id

    params["limit"] = limit

    params["offset"] = offset

    json_group = group

    params["group"] = json_group

    params["gameType"] = game_type

    params["season"] = season

    params["sportIds"] = sport_ids

    params["sortStat"] = sort_stat

    params["order"] = order

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
        "url": "/v1/stats",
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
    stats: Any,
    player_pool: str | Unset = UNSET,
    position: StatsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    order: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View standard statistics.

     **Description:**
     This endpoint returns standard statistics.

     **Return Includes:** Team, league, player statistics.

     **Required Parameters:** stats and group are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting


    Args:
        stats (Any):
        player_pool (str | Unset):
        position (StatsPosition | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        limit (int | Unset):
        offset (str | Unset):
        group (list[str]):
        game_type (str | Unset):
        season (str | Unset):
        sport_ids (int | Unset):
        sort_stat (str | Unset):
        order (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        stats=stats,
        player_pool=player_pool,
        position=position,
        team_id=team_id,
        league_id=league_id,
        limit=limit,
        offset=offset,
        group=group,
        game_type=game_type,
        season=season,
        sport_ids=sport_ids,
        sort_stat=sort_stat,
        order=order,
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
    stats: Any,
    player_pool: str | Unset = UNSET,
    position: StatsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    order: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View standard statistics.

     **Description:**
     This endpoint returns standard statistics.

     **Return Includes:** Team, league, player statistics.

     **Required Parameters:** stats and group are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.

     ---

     **Example of call with required parameters**

       https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting


    Args:
        stats (Any):
        player_pool (str | Unset):
        position (StatsPosition | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        limit (int | Unset):
        offset (str | Unset):
        group (list[str]):
        game_type (str | Unset):
        season (str | Unset):
        sport_ids (int | Unset):
        sort_stat (str | Unset):
        order (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        stats=stats,
        player_pool=player_pool,
        position=position,
        team_id=team_id,
        league_id=league_id,
        limit=limit,
        offset=offset,
        group=group,
        game_type=game_type,
        season=season,
        sport_ids=sport_ids,
        sort_stat=sort_stat,
        order=order,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
