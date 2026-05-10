from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.league_leader_container_rest_object import (
    LeagueLeaderContainerRestObject,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    leader_categories: list[str],
    sit_codes: list[str] | Unset = UNSET,
    game_types: list[str] | Unset = UNSET,
    stat_group: list[str] | Unset = UNSET,
    season: str | Unset = UNSET,
    league_ids: int | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_leader_categories = leader_categories

    params["leaderCategories"] = json_leader_categories

    json_sit_codes: list[str] | Unset = UNSET
    if not isinstance(sit_codes, Unset):
        json_sit_codes = sit_codes

    params["sitCodes"] = json_sit_codes

    json_game_types: list[str] | Unset = UNSET
    if not isinstance(game_types, Unset):
        json_game_types = game_types

    params["gameTypes"] = json_game_types

    json_stat_group: list[str] | Unset = UNSET
    if not isinstance(stat_group, Unset):
        json_stat_group = stat_group

    params["statGroup"] = json_stat_group

    params["season"] = season

    params["leagueIds"] = league_ids

    params["startDate"] = start_date

    params["endDate"] = end_date

    params["sportId"] = sport_id

    json_hydrate: list[str] | Unset = UNSET
    if not isinstance(hydrate, Unset):
        json_hydrate = hydrate

    params["hydrate"] = json_hydrate

    params["limit"] = limit

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/stats/leaders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | LeagueLeaderContainerRestObject | None:
    if response.status_code == 200:
        response_200 = LeagueLeaderContainerRestObject.from_dict(response.json())

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
) -> Response[Any | LeagueLeaderContainerRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    leader_categories: list[str],
    sit_codes: list[str] | Unset = UNSET,
    game_types: list[str] | Unset = UNSET,
    stat_group: list[str] | Unset = UNSET,
    season: str | Unset = UNSET,
    league_ids: int | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | LeagueLeaderContainerRestObject]:
    """View leaders for a statistic.

     **Description:**
     This endpoint returns statistical data for top performers  based on League Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns

     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns&hydrate=team

    Args:
        leader_categories (list[str]):
        sit_codes (list[str] | Unset):
        game_types (list[str] | Unset):
        stat_group (list[str] | Unset):
        season (str | Unset):
        league_ids (int | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        sport_id (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | LeagueLeaderContainerRestObject]
    """

    kwargs = _get_kwargs(
        leader_categories=leader_categories,
        sit_codes=sit_codes,
        game_types=game_types,
        stat_group=stat_group,
        season=season,
        league_ids=league_ids,
        start_date=start_date,
        end_date=end_date,
        sport_id=sport_id,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    leader_categories: list[str],
    sit_codes: list[str] | Unset = UNSET,
    game_types: list[str] | Unset = UNSET,
    stat_group: list[str] | Unset = UNSET,
    season: str | Unset = UNSET,
    league_ids: int | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | LeagueLeaderContainerRestObject | None:
    """View leaders for a statistic.

     **Description:**
     This endpoint returns statistical data for top performers  based on League Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns

     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns&hydrate=team

    Args:
        leader_categories (list[str]):
        sit_codes (list[str] | Unset):
        game_types (list[str] | Unset):
        stat_group (list[str] | Unset):
        season (str | Unset):
        league_ids (int | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        sport_id (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | LeagueLeaderContainerRestObject
    """

    return sync_detailed(
        client=client,
        leader_categories=leader_categories,
        sit_codes=sit_codes,
        game_types=game_types,
        stat_group=stat_group,
        season=season,
        league_ids=league_ids,
        start_date=start_date,
        end_date=end_date,
        sport_id=sport_id,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    leader_categories: list[str],
    sit_codes: list[str] | Unset = UNSET,
    game_types: list[str] | Unset = UNSET,
    stat_group: list[str] | Unset = UNSET,
    season: str | Unset = UNSET,
    league_ids: int | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | LeagueLeaderContainerRestObject]:
    """View leaders for a statistic.

     **Description:**
     This endpoint returns statistical data for top performers  based on League Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns

     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns&hydrate=team

    Args:
        leader_categories (list[str]):
        sit_codes (list[str] | Unset):
        game_types (list[str] | Unset):
        stat_group (list[str] | Unset):
        season (str | Unset):
        league_ids (int | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        sport_id (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | LeagueLeaderContainerRestObject]
    """

    kwargs = _get_kwargs(
        leader_categories=leader_categories,
        sit_codes=sit_codes,
        game_types=game_types,
        stat_group=stat_group,
        season=season,
        league_ids=league_ids,
        start_date=start_date,
        end_date=end_date,
        sport_id=sport_id,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    leader_categories: list[str],
    sit_codes: list[str] | Unset = UNSET,
    game_types: list[str] | Unset = UNSET,
    stat_group: list[str] | Unset = UNSET,
    season: str | Unset = UNSET,
    league_ids: int | Unset = UNSET,
    start_date: str | Unset = UNSET,
    end_date: str | Unset = UNSET,
    sport_id: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | LeagueLeaderContainerRestObject | None:
    """View leaders for a statistic.

     **Description:**
     This endpoint returns statistical data for top performers  based on League Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.


     ---
     **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns

     ---
     **Example of call with hydration parameters**

     https://statsapi.mlb.com/api/v1/teams/stats/leaders?leaderCategories=homeRuns&hydrate=team

    Args:
        leader_categories (list[str]):
        sit_codes (list[str] | Unset):
        game_types (list[str] | Unset):
        stat_group (list[str] | Unset):
        season (str | Unset):
        league_ids (int | Unset):
        start_date (str | Unset):
        end_date (str | Unset):
        sport_id (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | LeagueLeaderContainerRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            leader_categories=leader_categories,
            sit_codes=sit_codes,
            game_types=game_types,
            stat_group=stat_group,
            season=season,
            league_ids=league_ids,
            start_date=start_date,
            end_date=end_date,
            sport_id=sport_id,
            hydrate=hydrate,
            limit=limit,
            fields=fields,
        )
    ).parsed
