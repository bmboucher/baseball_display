from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.people_rest_object import PeopleRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    season: str,
    group: str,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["season"] = season

    params["group"] = group

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
        "url": "/v1/teams/{team_id}/alumni".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PeopleRestObject | None:
    if response.status_code == 200:
        response_200 = PeopleRestObject.from_dict(response.json())

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
) -> Response[Any | PeopleRestObject]:
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
    season: str,
    group: str,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PeopleRestObject]:
    """View all team alumni.

     **Description:**
     This endpoint allows you to return directory of active alumni for a given team.

     **Return Includes:** biogaphical information.

     **Required Parameters:** teamId,season & statGroup are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting

     ---
     **Example of call with hydrated parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting&hydrate=rosterEntries

    Args:
        team_id (str):
        season (str):
        group (str):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PeopleRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        season=season,
        group=group,
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
    season: str,
    group: str,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PeopleRestObject | None:
    """View all team alumni.

     **Description:**
     This endpoint allows you to return directory of active alumni for a given team.

     **Return Includes:** biogaphical information.

     **Required Parameters:** teamId,season & statGroup are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting

     ---
     **Example of call with hydrated parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting&hydrate=rosterEntries

    Args:
        team_id (str):
        season (str):
        group (str):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PeopleRestObject
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        season=season,
        group=group,
        hydrate=hydrate,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    group: str,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PeopleRestObject]:
    """View all team alumni.

     **Description:**
     This endpoint allows you to return directory of active alumni for a given team.

     **Return Includes:** biogaphical information.

     **Required Parameters:** teamId,season & statGroup are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting

     ---
     **Example of call with hydrated parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting&hydrate=rosterEntries

    Args:
        team_id (str):
        season (str):
        group (str):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PeopleRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        season=season,
        group=group,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient | Client,
    season: str,
    group: str,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PeopleRestObject | None:
    """View all team alumni.

     **Description:**
     This endpoint allows you to return directory of active alumni for a given team.

     **Return Includes:** biogaphical information.

     **Required Parameters:** teamId,season & statGroup are required to run this call.

     **Hydrations:** This endpoint can accept the hydrations query parameter.



     ---
     **Example of call with required parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting

     ---
     **Example of call with hydrated parameters**

     http://statsapi.mlb.com/api/v1/teams/147/alumni?season=2018&group=hitting&hydrate=rosterEntries

    Args:
        team_id (str):
        season (str):
        group (str):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PeopleRestObject
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            season=season,
            group=group,
            hydrate=hydrate,
            fields=fields,
        )
    ).parsed
