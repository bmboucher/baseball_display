from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    stats: Any,
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_id: int | Unset = UNSET,
    min_occurrences: int | Unset = UNSET,
    percentile: int | Unset = UNSET,
    person_id: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["stats"] = stats

    json_group = group

    params["group"] = json_group

    params["gameType"] = game_type

    params["season"] = season

    params["startDate"] = start_date

    params["endDate"] = end_date

    params["venueId"] = venue_id

    params["minOccurrences"] = min_occurrences

    params["percentile"] = percentile

    params["personId"] = person_id

    params["teamId"] = team_id

    params["limit"] = limit

    params["offset"] = offset

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
        "url": "/v1/stats/metrics",
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
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_id: int | Unset = UNSET,
    min_occurrences: int | Unset = UNSET,
    percentile: int | Unset = UNSET,
    person_id: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View Statcast stats.

     **Description:**
     This endpoint returns Statcast stats.

     **Return Includes:** Team, league, player statistics.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     **Required Parameters:** stats, metrics, season, and group are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/stats/metrics?stats=metricAverages&metrics=launchSpeed&group=hitti
    ng&season=2019


    Args:
        stats (Any):
        group (list[str]):
        game_type (str | Unset):
        season (str):
        start_date (str | Unset):
        end_date (str | Unset):
        venue_id (int | Unset):
        min_occurrences (int | Unset):
        percentile (int | Unset):
        person_id (int | Unset):
        team_id (int | Unset):
        limit (int | Unset):
        offset (str | Unset):
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
        group=group,
        game_type=game_type,
        season=season,
        start_date=start_date,
        end_date=end_date,
        venue_id=venue_id,
        min_occurrences=min_occurrences,
        percentile=percentile,
        person_id=person_id,
        team_id=team_id,
        limit=limit,
        offset=offset,
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
    group: list[str],
    game_type: str | Unset = UNSET,
    season: str,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    venue_id: int | Unset = UNSET,
    min_occurrences: int | Unset = UNSET,
    percentile: int | Unset = UNSET,
    person_id: int | Unset = UNSET,
    team_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View Statcast stats.

     **Description:**
     This endpoint returns Statcast stats.

     **Return Includes:** Team, league, player statistics.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     **Required Parameters:** stats, metrics, season, and group are required to run this call.

     ---

     **Example of call with required parameters**

       http://statsapi.mlb.com/api/v1/stats/metrics?stats=metricAverages&metrics=launchSpeed&group=hitti
    ng&season=2019


    Args:
        stats (Any):
        group (list[str]):
        game_type (str | Unset):
        season (str):
        start_date (str | Unset):
        end_date (str | Unset):
        venue_id (int | Unset):
        min_occurrences (int | Unset):
        percentile (int | Unset):
        person_id (int | Unset):
        team_id (int | Unset):
        limit (int | Unset):
        offset (str | Unset):
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
        group=group,
        game_type=game_type,
        season=season,
        start_date=start_date,
        end_date=end_date,
        venue_id=venue_id,
        min_occurrences=min_occurrences,
        percentile=percentile,
        person_id=person_id,
        team_id=team_id,
        limit=limit,
        offset=offset,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
