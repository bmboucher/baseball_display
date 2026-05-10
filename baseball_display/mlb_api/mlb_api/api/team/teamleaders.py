from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team_leader_container_rest_object import TeamLeaderContainerRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    leader_categories: str,
    season: str,
    leader_game_types: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["leaderCategories"] = leader_categories

    params["season"] = season

    params["leaderGameTypes"] = leader_game_types

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
        "url": "/v1/teams/{team_id}/leaders".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | TeamLeaderContainerRestObject | None:
    if response.status_code == 200:
        response_200 = TeamLeaderContainerRestObject.from_dict(response.json())

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
) -> Response[Any | TeamLeaderContainerRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    leader_categories: str,
    season: str,
    leader_game_types: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | TeamLeaderContainerRestObject]:
    """View statistical and biographical  information on stat leaders for a given club.

     **Description:**
     This endpoint returns statistical data for a team's top performers information based on League
    Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** teamdId,season, and leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018

     ---
     **Example of call with hydration parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018&hydrate=te
    am(league),hydrations

    Args:
        team_id (str):
        leader_categories (str):
        season (str):
        leader_game_types (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | TeamLeaderContainerRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        leader_categories=leader_categories,
        season=season,
        leader_game_types=leader_game_types,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    leader_categories: str,
    season: str,
    leader_game_types: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | TeamLeaderContainerRestObject | None:
    """View statistical and biographical  information on stat leaders for a given club.

     **Description:**
     This endpoint returns statistical data for a team's top performers information based on League
    Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** teamdId,season, and leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018

     ---
     **Example of call with hydration parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018&hydrate=te
    am(league),hydrations

    Args:
        team_id (str):
        leader_categories (str):
        season (str):
        leader_game_types (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | TeamLeaderContainerRestObject
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        leader_categories=leader_categories,
        season=season,
        leader_game_types=leader_game_types,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    leader_categories: str,
    season: str,
    leader_game_types: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | TeamLeaderContainerRestObject]:
    """View statistical and biographical  information on stat leaders for a given club.

     **Description:**
     This endpoint returns statistical data for a team's top performers information based on League
    Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** teamdId,season, and leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018

     ---
     **Example of call with hydration parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018&hydrate=te
    am(league),hydrations

    Args:
        team_id (str):
        leader_categories (str):
        season (str):
        leader_game_types (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | TeamLeaderContainerRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        leader_categories=leader_categories,
        season=season,
        leader_game_types=leader_game_types,
        hydrate=hydrate,
        limit=limit,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    leader_categories: str,
    season: str,
    leader_game_types: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | TeamLeaderContainerRestObject | None:
    """View statistical and biographical  information on stat leaders for a given club.

     **Description:**
     This endpoint returns statistical data for a team's top performers information based on League
    Leader Categories.

     **Return Includes:** Player biographical and statistical information.

     **Required Parameters:** teamdId,season, and leaderCategories is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018

     ---
     **Example of call with hydration parameters**

      https://statsapi.mlb.com/api/v1/teams/111/leaders?leaderCategories=homeRuns&season=2018&hydrate=te
    am(league),hydrations

    Args:
        team_id (str):
        leader_categories (str):
        season (str):
        leader_game_types (str | Unset):
        hydrate (list[str] | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | TeamLeaderContainerRestObject
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            leader_categories=leader_categories,
            season=season,
            leader_game_types=leader_game_types,
            hydrate=hydrate,
            limit=limit,
            fields=fields,
        )
    ).parsed
