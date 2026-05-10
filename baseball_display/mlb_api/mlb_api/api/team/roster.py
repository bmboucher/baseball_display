from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.roster_rest_object import RosterRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    roster_type: str,
    season: str,
    date: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["rosterType"] = roster_type

    params["season"] = season

    params["date"] = date

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
        "url": "/v1/teams/{team_id}/roster".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | RosterRestObject | None:
    if response.status_code == 200:
        response_200 = RosterRestObject.from_dict(response.json())

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
) -> Response[Any | RosterRestObject]:
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
    roster_type: str,
    season: str,
    date: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | RosterRestObject]:
    """View biographical and statistical information for a club's roster.


    **Description:**
     Insert teamId to return a directory of players based on roster status for a particular club.


     **Return Includes:** Player information for provided team.

     **Required Parameters:** teamId, season, & rosterType is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.






     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=Active

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?hydrate=person(stats(type=season,season=2018),educ
    ation)&rosterType=Active

    Args:
        team_id (str):
        roster_type (str):
        season (str):
        date (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RosterRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        roster_type=roster_type,
        season=season,
        date=date,
        hydrate=hydrate,
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
    roster_type: str,
    season: str,
    date: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | RosterRestObject | None:
    """View biographical and statistical information for a club's roster.


    **Description:**
     Insert teamId to return a directory of players based on roster status for a particular club.


     **Return Includes:** Player information for provided team.

     **Required Parameters:** teamId, season, & rosterType is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.






     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=Active

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?hydrate=person(stats(type=season,season=2018),educ
    ation)&rosterType=Active

    Args:
        team_id (str):
        roster_type (str):
        season (str):
        date (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RosterRestObject
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        roster_type=roster_type,
        season=season,
        date=date,
        hydrate=hydrate,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    roster_type: str,
    season: str,
    date: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | RosterRestObject]:
    """View biographical and statistical information for a club's roster.


    **Description:**
     Insert teamId to return a directory of players based on roster status for a particular club.


     **Return Includes:** Player information for provided team.

     **Required Parameters:** teamId, season, & rosterType is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.






     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=Active

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?hydrate=person(stats(type=season,season=2018),educ
    ation)&rosterType=Active

    Args:
        team_id (str):
        roster_type (str):
        season (str):
        date (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RosterRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        roster_type=roster_type,
        season=season,
        date=date,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    roster_type: str,
    season: str,
    date: str | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | RosterRestObject | None:
    """View biographical and statistical information for a club's roster.


    **Description:**
     Insert teamId to return a directory of players based on roster status for a particular club.


     **Return Includes:** Player information for provided team.

     **Required Parameters:** teamId, season, & rosterType is required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.






     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?rosterType=Active

     ---
     **Example of call with hydrated parameters**

     https://statsapi.mlb.com/api/v1/teams/109/roster?hydrate=person(stats(type=season,season=2018),educ
    ation)&rosterType=Active

    Args:
        team_id (str):
        roster_type (str):
        season (str):
        date (str | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RosterRestObject
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            roster_type=roster_type,
            season=season,
            date=date,
            hydrate=hydrate,
            fields=fields,
        )
    ).parsed
