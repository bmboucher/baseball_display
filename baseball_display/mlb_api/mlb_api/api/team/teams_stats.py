from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    season: str,
    sport_ids: str | Unset = UNSET,
    stat_group: str,
    game_type: str | Unset = UNSET,
    stats: str | Unset = UNSET,
    order: str | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["season"] = season

    params["sportIds"] = sport_ids

    params["statGroup"] = stat_group

    params["gameType"] = game_type

    params["stats"] = stats

    params["order"] = order

    params["sortStat"] = sort_stat

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/stats",
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
    season: str,
    sport_ids: str | Unset = UNSET,
    stat_group: str,
    game_type: str | Unset = UNSET,
    stats: str | Unset = UNSET,
    order: str | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View team stats.

     **Description:**
     This endpoint returns team statistics based on year,leagueId,sportId and gameType.

     **Return Includes:** team season statistics.

     **Required Parameters:** stat group, season, and stats are required to run this call



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/stats?group=hitting&stats=season&season=2018

    Args:
        season (str):
        sport_ids (str | Unset):
        stat_group (str):
        game_type (str | Unset):
        stats (str | Unset):
        order (str | Unset):
        sort_stat (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        sport_ids=sport_ids,
        stat_group=stat_group,
        game_type=game_type,
        stats=stats,
        order=order,
        sort_stat=sort_stat,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    season: str,
    sport_ids: str | Unset = UNSET,
    stat_group: str,
    game_type: str | Unset = UNSET,
    stats: str | Unset = UNSET,
    order: str | Unset = UNSET,
    sort_stat: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View team stats.

     **Description:**
     This endpoint returns team statistics based on year,leagueId,sportId and gameType.

     **Return Includes:** team season statistics.

     **Required Parameters:** stat group, season, and stats are required to run this call



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/stats?group=hitting&stats=season&season=2018

    Args:
        season (str):
        sport_ids (str | Unset):
        stat_group (str):
        game_type (str | Unset):
        stats (str | Unset):
        order (str | Unset):
        sort_stat (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        season=season,
        sport_ids=sport_ids,
        stat_group=stat_group,
        game_type=game_type,
        stats=stats,
        order=order,
        sort_stat=sort_stat,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
